exec { 'deploy management node':
  cwd => "python/modules",
  logoutput => true,
  command => "python deploy_mgmt.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
} ->
exec { 'waiting for nodes to be online and manage services':
  cwd => "python/modules",
  logoutput => true,
  command => "python manage_services.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}