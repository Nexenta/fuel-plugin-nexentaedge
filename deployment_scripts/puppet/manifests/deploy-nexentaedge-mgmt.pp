exec { 'deploy management node':
  logoutput => true,
  command => "python python/modules/deploy_mgmt.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
} ->
exec { 'waiting for nodes to be online and manage services':
  logoutput => true,
  command => "python python/modules/manage_services.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}