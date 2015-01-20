#!/bin/bash
# http://stackoverflow.com/questions/7975556/how-to-start-postgresql-server-on-mac-os-x
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
