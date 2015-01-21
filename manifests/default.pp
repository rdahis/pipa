include apt

class { 'postgresql::globals':
	manage_package_repo => true,
	version             => '9.4',
}->
class { 'postgresql::server':
}
postgresql::server::db { 'DP':
	user => 'vagrant',
	password => ''
}

package {
	'git':
	ensure => latest
	;'bash-completion':
	ensure => present
}
