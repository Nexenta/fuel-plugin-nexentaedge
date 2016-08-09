include nexentaedge

$settings = hiera("fuel-plugin-nexentaedge")
exec { 'deploy management node':
  cwd => "${nexentaedge::root_path}python/modules",
  logoutput => true,
  command => "python deploy_mgmt.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
} ->
exec { 'wait for being online and manage services':
  cwd => "${nexentaedge::root_path}python/modules",
  logoutput => true,
  command => "python manage_services.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}