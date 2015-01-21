include apt

apt::key { 'postgresql':
	key        => 'ACCC4CF8',
	key_source => 'https://www.postgresql.org/media/keys/ACCC4CF8.asc',
}
apt::source { "postgresql":
	location        => "http://apt.postgresql.org/pub/repos/apt/",
	release         => "${::lsbdistcodename}-pgdg",
	repos           => "main",
}
package {
	"git":
		ensure => present
		;
	"postgresql-9.4":
		ensure => present
}
