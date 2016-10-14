exec { 'get neadm':
  logoutput => true,
  command => "python python/modules/get_neadm.py",
  path => "/usr/bin"
}