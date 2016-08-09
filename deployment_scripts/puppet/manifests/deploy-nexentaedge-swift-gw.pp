include nexentaedge

exec { 'deploy swift node':
  cwd => "${nexentaedge::root_path}python/modules",
  logoutput => true,
  command => "python deploy_iscsi_gw.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}
