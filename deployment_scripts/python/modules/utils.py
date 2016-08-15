import netifaces
import yaml
import requests
import shutil
import time

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


def download(url, path):
    max_attempts = 10
    attempts = 0
    while True:
        r = requests.get(url, stream=True)
        try:
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                break
            else:
                if r.status_code == 503 and attempts < max_attempts:
                    attempts += 1
                    time.sleep(5)
                    continue
                msg = 'An error occured while trying to download file at ' \
                      '{}. Code: {}, Reason: {}'.format(
                       url, r.status_code, r.reason)
                raise requests.HTTPError(msg)
        finally:
            r.close()
