exec { 'Restore Fuel apt list':
  command => "mv -f /etc/apt/sources.list.d/fuel-plugin-nexentaedge-1.0.0.list.nedge-backup /etc/apt/sources.list.d/fuel-plugin-nexentaedge-1.0.0.list 2>/dev/null || true",
  path => "/bin"
} ->

exec { 'Delete standard ubuntu trusty apt list':
  command => "rm /etc/apt/sources.list.d/ubuntu-trusty-apt.list 2>/dev/null || true",
  path => "/bin"
} ->

exec { 'Delete force_confdef':
  command => "rm /etc/apt/apt.conf.d/force_confdef 2>/dev/null || true",
  path => "/bin"
} ->

exec { "apt-get update":
  command => "apt-get update",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
}