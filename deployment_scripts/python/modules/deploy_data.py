import sys
from nexentaedge.utils import get_sid
from nexentaedge.nedgeConfigurator import NedgeNodeConfigurator
from utils import get_iface_name_by_mac_from_list
from utils import get_deployment_config


def main():
    # check nedge already installed and ready
    if get_sid():
        return

    cfg = get_deployment_config()
    plugin = cfg['fuel-plugin-nexentaedge']
    replicast_name = get_iface_name_by_mac_from_list(plugin['replicast_macs'])

    environment = {
        'node_private_ip': '127.0.0.1',
        'replicast_eth': replicast_name,
        'profile': plugin['profile'],
        'nodocker': plugin['nodocker'],
        'exclude': None,
        'reserved': None
    }

    configurator = NedgeNodeConfigurator(environment)

    if not configurator.configure():
        blockers = configurator.get_blockers()
        if blockers:
            print('blocked')
            for blocker in blockers:
                print(blocker)
        sys.exit(1)


if __name__ == '__main__':
    main()
