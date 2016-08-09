include nexentaedge

exec { 'get neadm':
  cwd => "${nexentaedge::root_path}python/modules",
  logoutput => true,
  command => "python get_neadm.py",
  path => "/usr/bin"
}