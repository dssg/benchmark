FROM postgres:9.6
COPY pg.conf /etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]

## PostGIS activation
RUN apt-get -y update \
    && apt-get -y  install wget \
    && wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add - \
    && apt-get -y update \
    && apt-get -y install postgresql-9.6-postgis-2.3 postgis postgresql-9.6-pgrouting \ 
    && apt-get -y install python3-yaml \
    && apt-get -y install python3-psycopg2 \
    && apt-get -y install python3-sqlalchemy \
    && apt-get -y install python3-numpy python3-dateutil  \
    && apt-get -y install python3-pip \
    && pip3 install pandas
    

## DB setup
ADD activate_postgis.sql /docker-entrypoint-initdb.d/
ADD create_extensions.sql /docker-entrypoint-initdb.d/
ADD create_tables/ /docker-entrypoint-initdb.d/create_tables/

ADD init.sh /docker-entrypoint-initdb.d/

ADD lookup_tables.yaml /docker-entrypoint-initdb.d/
ADD populate_lookup_tables.py /docker-entrypoint-initdb.d/ 
ADD create_and_load_etl_data.script /docker-entrypoint-initdb.d/
 

RUN chown -R postgres:postgres /docker-entrypoint-initdb.d/*.sql
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
#RUN chown postgres:postgres /docker-entrypoint-initdb.d/create_tables/*.sql
