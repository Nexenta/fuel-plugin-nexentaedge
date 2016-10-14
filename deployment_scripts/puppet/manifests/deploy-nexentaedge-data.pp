exec { 'deploy data node':
  logoutput => true,
  command => "python python/modules/deploy_data.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  timeout => 900
}
