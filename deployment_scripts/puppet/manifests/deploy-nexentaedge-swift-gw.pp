exec { 'deploy swift gateway node':
  logoutput => true,
  command => "python python/modules/deploy_iscsi_gw.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}
