include apt
$PROJECT_ROOT = '/DP'
$BACKPORTS = '/wheezy-backports'

apt::source { 'debian_backports':
	location          => 'http://http.debian.net/debian',
	release           => 'wheezy-backports',
	repos             => 'main',
}

class { 'postgresql::globals':
	manage_package_repo => true,
	version             => '9.4',
	encoding => 'UTF8',
}->
class { 'postgresql::server':
	encoding => 'UTF8',
	locale => 'en_US.UTF-8',
	listen_addresses => '*',
	ip_mask_deny_postgres_user => '0.0.0.0/32',
	ip_mask_allow_all_users    => '0.0.0.0/0',
}
postgresql::server::db { 'DP':
	user => 'vagrant',
	password => '.',
}


package {
	"git${BACKPORTS}":
		ensure => latest
		require => Apt::Source['debian_backports']
	;'python2.7':
		ensure => present
	;'bash-completion':
		ensure => present
}

package {
	'postgresql-server-dev-9.4':
		ensure => present,
		require => Class['postgresql::server']
	;'python2.7-dev':
		ensure => present
	;'python-pip':
		ensure => present
	;'libxml2-dev':
		ensure => present
	;'libxslt1-dev':
		ensure => present
}
->
python::requirements { "${PROJECT_ROOT}/scrap/requirements.txt" :
}
