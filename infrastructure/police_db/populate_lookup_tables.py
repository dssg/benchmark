#!/usr/bin/env python

"""Script to populate lookup tables using the information stored in a yaml file"""

import argparse
import yaml
import pandas as pd
import psycopg2
import sqlalchemy
import os


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tablefile", help="the yaml table definition file")
parser.add_argument("-s", "--schema", help="name of the staging schema", default="staging")
args = parser.parse_args()




# establish a connection to the database
engine = sqlalchemy.create_engine('postgresql://{user}:{password}@{host}/{database}'.format(
                           host = os.environ['POSTGRES_HOST'],
                           database = os.environ['POSTGRES_DB'], 
                           user = os.environ['POSTGRES_USER'],
                           password = os.environ['POSTGRES_PASSWORD']))
db_conn = engine.connect()

# read the lookup table data from the yaml file
with open(args.tablefile) as infile:
    table_dict = yaml.load(infile.read())

# populate each table
for table_name, contents in table_dict.items():

    # remove all rows from the table, if any are already present
    sql_query = """DELETE FROM {}.{}""".format(args.schema, table_name)
    db_conn.execute(sql_query)

    table_df = pd.DataFrame(contents['rows'], columns=contents['columns'])
    table_df.to_sql(table_name, db_conn, index=False, schema=args.schema, if_exists='append')
    print('done with {}'.format(table_name))
