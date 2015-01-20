#!/bin/bash
if [ -f /etc/init.d/postgresql ]; then
	/etc/init.d/postgresql stop
else
	pg_ctl -D /usr/local/var/postgres stop -s -m fast
fi;
