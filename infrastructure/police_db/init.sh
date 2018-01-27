#!/bin/bash
set -e

RUN_DB="psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" police_db" 

$RUN_DB <<SQL
DROP SCHEMA IF EXISTS staging CASCADE;
CREATE SCHEMA staging;
SQL


cd /docker-entrypoint-initdb.d/create_tables

for dir in `ls` 
do
	echo "$dir"
	$RUN_DB -f $dir
done


