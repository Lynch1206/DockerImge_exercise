#%%
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# SQLite connection
sqlite_conn = sqlite3.connect('stock.db')

# Fetch table names from SQLite
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
sqlite_tables = sqlite_cursor.fetchall()

# PostgreSQL connection parameters
pg_params = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': '123',
    'host': 'localhost',  # Use 'localhost' since Docker container is accessed from the host
    'port': 5432
}

# Create SQLAlchemy engine for PostgreSQL
pg_engine = create_engine(f"postgresql+psycopg2://{pg_params['user']}:{pg_params['password']}@{pg_params['host']}:{pg_params['port']}/{pg_params['dbname']}")

# Connect to PostgreSQL using psycopg2 for compatibility
pg_conn = psycopg2.connect(**pg_params)
pg_cursor = pg_conn.cursor()

# Load each table from SQLite into PostgreSQL
for table_name in sqlite_tables:
    table_name = table_name[0]  # Extract table name from tuple
    print(f"Loading table: {table_name}")

    # Read table from SQLite into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)

    # Write DataFrame to PostgreSQL using SQLAlchemy
    df.to_sql(table_name, pg_engine, if_exists='replace', index=False)
    print(f"Table '{table_name}' written to PostgreSQL.")

# make commit to save the changes in container
pg_conn.commit()

# Close SQLite connection
sqlite_conn.close()

# Close PostgreSQL cursor and connection
pg_cursor.close()
pg_conn.close()

# Instructions to save the updated state of the Docker container as a new image
print("Now commit the updated Docker container to a new image using:")
print("docker commit pg-container mypostgresql-image")
# %%
# parse the tables from the docker container
#%%
import psycopg2
from psycopg2 import sql
import pandas as pd

# Define your connection parameters
pg_params = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': '123',
    'host': 'localhost',  # Use 'localhost' since Docker container is accessed from the host
    'port': 5432
}

#%%
pg_conn = psycopg2.connect(**pg_params)
pg_cursor = pg_conn.cursor()

# list all tables
pg_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
# Fetch all table names
tables = pg_cursor.fetchall()

import pandas as pd
for table in tables:
    print(table[0])
#%%
# export all tables as dataframe
dfs = {}
for table in tables:
    table_name = table[0]
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", pg_conn)
    dfs[table_name] = df

# print out the heads of the dataframes
for table, df in dfs.items():
    print(f"Table: {table}")
    print(df.head(3))
    print()