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
		ensure => latest,
		require => Apt::Source['debian_backports']
	;'python2.7':
		ensure => present
	;'bash-completion':
		ensure => present,
}

file { '/etc/profile.d/dp-append-path.sh':
	mode    => 644,
	content => "PATH=\$PATH:${PROJECT_ROOT}/bin; export PYTHONPATH=\$PYTHONPATH:$PROJECT_ROOT",
}

exec { 'activate-global-python-argcomplete':
	command => 'activate-global-python-argcomplete',
	path => ['/usr/local/bin', '/usr/bin'],
	creates => '/etc/bash_completion.d/python-argcomplete.sh'
}
exec {'scrapy-autocomplete':
	command => 'wget https://raw.githubusercontent.com/scrapy/scrapy/master/extras/scrapy_bash_completion -O /etc/bash_completion.d/scrapy',
	path => ['/usr/local/bin', '/usr/bin'],
	creates => '/etc/bash_completion.d/scrapy'
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
python::requirements { "${PROJECT_ROOT}/requirements.txt" :
}

tidy { 'clean_pyc':
	path => $PROJECT_ROOT,
	matches => '*.pyc',
	age => 0,
	recurse => inf
}

/*
package {
	#;'python3-pip':
	#	ensure => present,
	#;'python3-dev':
	#	ensure => present,
}
class { 'python' :
	version    => '3.2',
	pip        => true,
	dev        => true,
	virtualenv => true,
}
->
exec { "pip":
	command => "/usr/bin/easy_install-2.7 --upgrade pip"
}

$path_requirements_file = "$PROJECT_ROOT/combiner/requirements.txt"
file { $path_requirements_file:
		checksum => 'md5',
		ensure => exists,
		notify => Exec["pip_requirements_install"],
}

exec { "pip_requirements_install":
	command     => "/usr/bin/pip-3.2 install -r ${path_requirements_file}",
	refreshonly => true,
}
*/
