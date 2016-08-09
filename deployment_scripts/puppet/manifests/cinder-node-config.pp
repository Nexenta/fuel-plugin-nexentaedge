exec {'config cinder.conf':
  command => "python python/modules/cinder_config.py",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}