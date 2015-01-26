#!/bin/bash
sudo -u postgres psql DP -c 'DROP SCHEMA public CASCADE;'
psql DP -c 'CREATE SCHEMA public;'
