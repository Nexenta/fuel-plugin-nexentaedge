import ConfigParser
import subprocess
from utils import get_deployment_config, download

CINDER_PATH = '/etc/cinder/cinder.conf'


def get_raw_output(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return 0, output
    except subprocess.CalledProcessError as ex:
        return ex.returncode, ex.output


def main():
    cfg = get_deployment_config()
    plugin = cfg['fuel-plugin-nexentaedge']
    if plugin['use_cinder']:

        # getting the driver from Nexenta repo if its version is in the list
        branches = ('liberty', 'mitaka')
        version = filter(lambda branch: branch in cfg['openstack_version'],
                         branches)
        if version:
            version = version[0]
            branch = 'stable/' + version
            url_prefix = 'https://raw.githubusercontent.com/Nexenta/cinder/' \
                         '{}/cinder/volume/drivers/nexenta'.format(branch)
            local_path = '/usr/lib/python2.7/dist-packages/cinder/volume/' \
                         'drivers/nexenta'
            filenames = ['nexentaedge/iscsi.py', 'nexentaedge/jsonrpc.py',
                         'nexentaedge/__init__.py', 'options.py', 'utils.py']
            for name in filenames:
                download(
                    '/'.join((url_prefix, name)),
                    '/'.join((local_path, name)))

        nodes = cfg['nodes']

        config = ConfigParser.RawConfigParser()
        config.read(CINDER_PATH)

        mgmt_node = filter(lambda node: node['role'] == 'nexentaedge-mgmt',
                           nodes)
        if len(mgmt_node) != 1:
            raise Exception('Wrong NexentaEdge management nodes count. '
                            'It must be equal 1.')
        mgmt_node_ip = mgmt_node[0]['internal_address']

        volume_backend_name = 'nedge'

        enabled_backends = set(map(
            lambda name: name.strip(),
            config.defaults().get('enabled_backends', '').split(',')))

        nodes = filter(lambda node: node['role'] == 'nexentaedge-iscsi-gw',
                       nodes)

        # Remove old nodes
        for section in config.sections():
            if config.has_option(section, 'volume_backend_name') \
                and config.get(section,
                               'volume_backend_name') == volume_backend_name \
                    and not filter(lambda node: node['name'] == section[len(
                        volume_backend_name) + 1:], nodes):
                config.remove_section(section)
                if section in enabled_backends:
                    enabled_backends.remove(section)

        # Add new nodes
        for node in nodes:
            backend = '{}-{}'.format(volume_backend_name, node['name'])
            if not config.has_section(backend):
                config.add_section(backend)
            config.set(backend, 'iscsi_helper', 'tgtadm')
            config.set(backend, 'volume_group', 'nedge-volumes')
            config.set(backend, 'volume_backend_name', volume_backend_name)
            config.set(backend, 'nexenta_rest_address', mgmt_node_ip)
            config.set(
                backend,
                'volume_driver',
                'cinder.volume.drivers.nexenta.nexentaedge.'
                'iscsi.NexentaEdgeISCSIDriver')
            config.set(backend, 'nexenta_rest_port', '8080')
            config.set(backend, 'nexenta_rest_protocol', 'auto')
            config.set(backend, 'nexenta_iscsi_target_portal_port', '3620')
            config.set(backend, 'nexenta_rest_user', 'admin')
            config.set(backend, 'nexenta_rest_password', 'nexenta')
            config.set(backend,
                       'nexenta_lun_container',
                       '/'.join((plugin['cluster_name'], plugin['tenant_name'],
                                 plugin['bucket_name'])))
            config.set(backend, 'nexenta_iscsi_service', plugin['iscsi_name'])
            config.set(backend, 'nexenta_client_address',
                       node['internal_address'])
            enabled_backends.add(backend)

        config.set('DEFAULT', 'enabled_backends', ','.join(enabled_backends))
        config.set('DEFAULT', 'default_volume_type', volume_backend_name)

        # Fuel bug workaround.
        config.remove_option('DEFAULT', 'verbose')

        with open(CINDER_PATH, 'w') as f:
            config.write(f)

        access = cfg['access']
        creds = ['--os-auth-url={}'.format(
            config.defaults()['os_privileged_user_auth_url']),
            '--os-username={}'.format(access['user']),
            '--os-password={}'.format(access['password']),
            '--os-tenant-name={}'.format(access['tenant'])]

        command = ['cinder'] + creds + ['type-create', volume_backend_name]
        code, output = get_raw_output(command)
        if code and output.find('Volume Type {} already exists'.format(
                volume_backend_name)) == -1:
            raise Exception(output)
        command = ['cinder'] + creds + ['type-key', volume_backend_name, 'set',
                                        'volume_backend_name={}'.format(
                                            volume_backend_name)]
        subprocess.call(command)
        command = ['service', 'cinder-volume', 'restart']
        subprocess.call(command)


if __name__ == '__main__':
    main()
