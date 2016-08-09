import requests
import time
import re
from utils import get_deployment_config

from nexentaedge.neadmServiceWrapper import NeadmServiceWrapper

USER = 'admin'
PASSWORD = 'nexenta'


def get_table(text):
    text = text.strip('\n')
    lines = text.split('\n')
    rows = []
    header = lines[0]
    words = [word.strip() for word in header.split(' ') if word]
    for line in lines[1:]:
        row = {}
        for i in xrange(len(words)):
            word = words[i]
            start = header.index(word)
            if i == len(words) - 1:
                row[word] = line[start:]
            else:
                row[word] = line[start:header.index(words[i+1])]
            row[word] = row[word].strip()
        rows.append(row)
    return rows


class MockDict(dict):
    def set(self, key, value):
        self[key] = value


def main():
    cfg = get_deployment_config()
    plugin = cfg['fuel-plugin-nexentaedge']
    deployment_nodes = cfg['nodes']

    mock = MockDict(services=[])
    wrapper = NeadmServiceWrapper(mock)
    nedge_services = wrapper.get_all_services()
    if wrapper.exit_code and nedge_services.output.find('No services found') == -1:
        raise Exception(nedge_services.output)

    nedge_deployment_nodes = filter(lambda node: node['role'].find('nexentaedge') != -1, deployment_nodes)
    hostnames = dict.fromkeys([node['fqdn'] for node in nedge_deployment_nodes], None)
    t = time.clock()
    while True:
        output = wrapper.get_raw_output(['/opt/nedge/neadm/neadm', 'system', 'status'])
        ansi_escape = re.compile(r'\x1b[^m]*m')
        output = ansi_escape.sub('', output)
        neadm_nodes = get_table(output)
        count = 0
        for hostname in hostnames:
            n = filter(lambda node: node['ZONE:HOST'].find(hostname) != -1, neadm_nodes)
            if n:
                if n[0]['STATE'] == 'ONLINE':
                    count += 1
                elif n[0]['STATE'] == 'FAULTED':
                    raise Exception('Node {} is in FAULTED state'.format(hostname))
        if count == len(hostnames):
            print('All nodes are online')
            for hostname in hostnames:
                n = filter(lambda node: node['ZONE:HOST'].find(hostname) != -1, neadm_nodes)
                hostnames[hostname] = n[0]['SID']
            break
        elif time.clock() - t >= 5 * 60 * 1000:
            raise Exception('Time out')

    if plugin['use_iscsi']:
        found = False
        wrapper.create_iscsi_service(plugin['iscsi_name'])
        for node in nedge_deployment_nodes:
            if node['role'] == 'nexentaedge-iscsi-gw':
                wrapper.add_node_to_service(plugin['iscsi_name'], hostnames[node['fqdn']], None)
                found = True
        if found:
            wrapper.enable_service(plugin['iscsi_name'])

    if plugin['use_swift']:
        found = False
        wrapper.create_swift_service(plugin['swift_name'])
        for node in nedge_deployment_nodes:
            if node['role'] == 'nexentaedge-swift-gw':
                wrapper.add_node_to_service(plugin['swift_name'], hostnames[node['fqdn']], None)
                found = True
        if found:
            wrapper.serve_service(plugin['swift_name'], plugin['cluster_name'])
            wrapper.enable_service(plugin['swift_name'])


if __name__ == '__main__':
    main()
