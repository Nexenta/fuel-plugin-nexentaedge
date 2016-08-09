class nexentaedge::params
{
    $settings         = hiera('fuel-plugin-nexenta-edge')
    $replicast_macs   = $settings['replicast_macs']
    $cluster_name     = $settings['cluster_name']
    $tenant_name      = $settings['tenant_name']
    $bucket_name      = $settings['bucket_name']
    $iscsi_name       = $settings['iscsi_name']
    $swift_name       = $settings['swift_name']
    $activation_key   = $settings['activation_key']
    $use_cinder       = $settings['use_cinder']
    $use_swift        = $settings['use_swift']
    $mgmt_ip          = hiera('internal_address')

    $replicast_interface    = get_replicast_iface($replicast_macs)
    $node_count             = get_nedge_node_count()
    $nedge_mgmt_node_ip     = get_mgmt_node_ip()
}