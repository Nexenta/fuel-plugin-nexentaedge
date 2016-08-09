import netifaces
import yaml

YAML_PATH = '/etc/astute.yaml'


def get_iface_name_by_mac(mac):
    for interface_name in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface_name)
        if addrs:
            for addr in addrs[netifaces.AF_LINK]:
                if 'addr' in addr and addr['addr'] == mac:
                    return interface_name


def get_iface_name_by_mac_from_list(macs):
    for mac in macs.split(','):
        eth_name = get_iface_name_by_mac(mac.strip())
        if eth_name:
            return eth_name
    raise Exception('Replicast interface MAC address is not in the list')


def get_deployment_config():
    with open(YAML_PATH, 'r') as ymlfile:
        return yaml.load(ymlfile)