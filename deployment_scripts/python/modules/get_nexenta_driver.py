from utils import get_deployment_config


cfg = get_deployment_config()
branches = ('liberty', 'mitaka')
version = filter(lambda branch: cfg['openstack_version'].find(branch) != -1, branches)
