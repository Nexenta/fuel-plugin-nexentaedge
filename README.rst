=====================================
Fuel Plugin for NexentaEdge 1.1.0 FP3
=====================================
This plugin facilitiates the deployment and intitialization of NexentaEdge cluster, configuration of Cinder and Swift backends, deployment of Cinder Volume Driver and it's configuration.

:Version: 1.0
:MOS Fuel Version: 9.0
:Openstack Version: Mitaka
:NexentaEdge Version: 1.1.0 FP3

This document provides instructions for deploying, configuring, troubleshooting and using the NexentaEdge Plugin for Fuel 9.0.

------------
Requirements
------------
* Dedicated Replicast Network is required (10GBE is recommended). The Replicast network must be on a separate VLAN, or be a physically separate network. Each node will have a dedicated interfaces for Replicast. It will use IPv6 subnet that has no ingress or egress routes. Replicast network requires jumbo frames to be enabled (9000 MTU)
* Each Data Node requires 4 drives + system drive (SSD is optional)
* 64 bit architecture with a CPU that supports SSE4.2 (full SIMD instruction set extension), 4 cores
* 16GB RAM per data node, and 48GB per gateway node. If a node will function both as a data node and gateway node, Nexenta recommends at least 64GB RAM
* See NEdge Install Guide for more info (add missing link)

-----------
Limitations
-----------
* No Separate Gateways, always shared with NEdge Data Nodes
* No iSCSI HA support
* No S3 Support

---------
Licensing
---------
To deploy NexentaEdge cluster using fuel plugin, once must provide a license activation token for NexentaEdge. The token can be requested from `sales@nexenta.com <mailto://sales@nexenta.com>`_. This token has to be specified under Settings "Other".

---------
Deploying
---------
1. Download .rpm file (e.g. fuel-plugin-nexentaedge-1.0-1.0.0-1.noarch.rpm) from repo onto your Fuel master node
2. Exxecute fuel plugins --install fuel-plugin-nexentaedge-1.0-1.0.0-1.noarch.rpm
3. Create an envronment in your Fuel dashboard, enable the plugin in "Settings -> Other" the section and configure it. You must specify lisence activation key. It will be applied on management node. Also you must specify MAC addresses of Replicast interfaces for each node. You can find description of these options and other ones in "Settings -> Other" section.
4. Add nodes. The cluster must have the only management node.
5. Configure nodes. Each node must have at least 4 unlocated physical disks. Click Disk Configuration button and mark the appropriate disks as unallocated

------------
How it works
------------
When Fuel deploys NexentaEdge cluster, a script on management node waits for other NexentaEdge nodes to be deployed and if some of the nodes has faulted state, the script raises an exception and deployment process is stopped. If there are no errors, the script creates iSCSI and Swift service groups and adds the respective gateways to these groups. After that on each of the cinder nodes, the script configures cinder.conf using multi-backend mode and restarts cinder-volume service.

To add new node you need to do everything as usually and click 'Deploy Changes' button on Dashboard tab. Don't choose nodes you want to deploy, don't choose 'Deployment Only' option etc. Just click 'Deploy Changes'. It will enable you to redeploy whole cluster and consequently reconfigure NexentaEdge iSCSI and swift service groups and cinder.conf.

---------------
Troubleshooting
---------------
If the cluster is deployed but something is not working, login to Fuel master node, execute
    fuel nodes

Find the NexentaEdge mgmt address and login to it by executing
    ssh <mgmt_address>, where mgmt_address is an address of mgmt node from the table

Execute on mgmt node
    /opt/nedge/neadm/neadm system status

Thus you can see the status of your cluster. Pay attention to DEVs the column. Two numerics must coincide with the number of unallocated disks. If it is not so, check system requirements - maybe CPU has unsufficient number of cores or you forgot to specify unallocated disks. Also disks can be damaged or not to be physically unallocated. In this case you should replace the disks or erase any partitions

To use NexentaEdge CLI just execute
    /opt/nedge/neadm/neadm

and get help for how to use it.

NexentaEdge documentation `link <http://docs.nexenta.com/NexentaRH/server?%26area%3Dnedge_1.1%26mgr%3Dagm%26agt%3Dwsm%26wnd%3Dnedge_UG%7CNewWindow%26tpc%3D%2FNexentaRH%2FNexentaRH%2Fserver%2Fnedge_1.1%2Fprojects%2Fnedge_UG%2FNexentaEdge_Documentation.htm%3FRINoLog28301%3DT%26ctxid%3D%26project%3Dnedge_UG>`_.
