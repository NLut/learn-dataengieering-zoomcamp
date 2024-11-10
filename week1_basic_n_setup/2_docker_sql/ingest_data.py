#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host #host name
    port = params.port 
    db = params.db #db name
    table_name = params.table_name
    url = params.url
    i_name = "yellow_taxi.parquet"
    o_name = "yellow_taxi.csv"

    

    os.system(f"wget {url} -O {i_name}") # download file
    os.system(f"python parquet_to_csv.py -i {i_name} -o {o_name}") # convert from parquet to csv
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}') # create engine to connect to postgres

    df_iter = pd.read_csv(o_name, iterator=True, chunksize=100000) # read as chunk and itterable

    df = next(df_iter)

    # convert to datetime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace') # Create table with no record by table head.

    df.to_sql(name=table_name, con=engine, if_exists='append') # add record


    for i in range(2):
        t_start = time()
        
        df = next(df_iter) # move to another chunk or record

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args() # create args namespace

    main(args)
