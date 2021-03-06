exec { 'Backup Fuel apt list':
  command => "mv /etc/apt/sources.list.d/fuel-plugin-nexentaedge-1.0.0.list /etc/apt/sources.list.d/fuel-plugin-nexentaedge-1.0.0.list.nedge-backup 2>/dev/null || true",
  path => "/bin"
} ->

file { 'Copy standard ubuntu trusty apt list':
  source => "puppet:///modules/nexentaedge/ubuntu-trusty-apt.list",
  ensure => present,
  path => "/etc/apt/sources.list.d/ubuntu-trusty-apt.list"
} ->

exec { 'Backup iface config':
  command => "cp -f /etc/network/interfaces /etc/network/interfaces.nedge-backup 2>/dev/null || true",
  path => "/bin"
} ->

file { '/etc/apt/apt.conf.d/force_confdef':
  ensure  => file,
  content => 'Dpkg::Options {"--force-confdef";"--force-confold";}',
} ->

exec { "apt-get update":
  command => "apt-get update",
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
} ->

package { "python-pip":
  ensure => present
} ->

# install python libs
exec { "install nexentaedghe lib":
  cwd => "/etc/fuel/plugins/fuel-plugin-nexentaedge-1.0/python/dist/JujuCharm-master",
  command => "python setup.py install",
  path => "/usr/bin"
} ->
package { 'netifaces':
  ensure => present,
  provider => 'pip'
} ->
package { 'requests':
  ensure => present,
  provider => 'pip'
} ->
exec { 'get nedeploy':
  logoutput => true,
  command => "python python/modules/get_nedeploy.py",
  path => "/usr/bin"
}