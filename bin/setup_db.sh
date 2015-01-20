#!/bin/bash
set -e
./pgsql_start.sh
createdb DP
rake db:schema:load
