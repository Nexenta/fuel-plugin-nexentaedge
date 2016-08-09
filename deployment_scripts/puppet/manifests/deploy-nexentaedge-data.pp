include nexentaedge

$settings = hiera("fuel-plugin-nexentaedge", {})
exec { 'deploy data node':
  cwd => "${nexentaedge::root_path}python/modules",
  logoutput => true,
  command => "python deploy_data.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}
