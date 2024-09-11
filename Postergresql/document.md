# Basic interactions between sql and docker container using python and bash

## Establish the database

### Sqlite3
Python 3 is already embedded with sqlite3. But I want to get familiar with postergresql more. <br/>
Nevertheless, this time, I want to spend more time on the connections between modules instead of the SQL or parsing skills. Therefore, I use sqlite3 and parse data with `yfinance` to create a local database file, named: [`stock.db`](./stock.db). <br/>

Parsing file and export local database script see [`sq3_stock.py`](./sq3_stock.py)
> Some basic SQL operations in [sciprt](./SQL_practice.py).

> In the future, I will try to create a notebook addresses using cloud SQL tool.

### docker
The good thing about using Postergresql with docker is that we do not need to install the software locally.

- Approach Postergresql with docker
`docker run --name MyPostgres -d -p 5432:5432 -v ~/Postgres:/var/lib/postgresql/data -e POSTGRES_DB=eflab -e POSTGRES_USER=admin -e POSTGRES_PASSWORD='12345' postgres:latest`

> 使用 docker run 由 image 建立 container，當 Docker 發現本機沒有 image，會自動從 Docker Hub 下載。

`-name`：替 container 取一個人能夠識別的名字 MyPostgres (若省略，Docker 會自動以亂數建立 )
`-d` : detach，建立 container 後，就脫離目前 process

`-v` : volume，PostgresSQL 新增的資料會寫在 container 內的 /var/lib/postgresql/data 目錄，會改 mapping 到 host 的 ~/Postgres，如此 container 刪除後，資料仍然會留在 host

`-p` : port mapping，host 與 container post 的對應，格式為 host port : container port
`-e` : environment，設定 PostgreSQL 所需要的環境變數
```
POSTGRES_DB : database 名稱
POSTGRES_USER : 帳號
POSTGRES_PASSWORD : 密碼
postgress:latest : image 名稱，其中 latest 為最新版的 image
```

```
docker run --name MyPostgres -d -p 5432:5432 -v ~/Postgres:/var/lib/postgresql/data -e POSTGRES_DB=eflab -e POSTGRES_USER=admin -e POSTGRES_PASSWORD='12345' postgres:latest
```

```
docker run --name pg-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
```

Use `pgloader` for loading a local database file for the postergresql container.

`brew install pgloader`

Use pgloader to migrate the data, the `path/to` should be modified.
```
pgloader sqlite://path/to/stock.db postgresql://myuser:mypassword@localhost:5432/mydatabase
```

## 用sqlite3 製作資料然後用python3去寫入 postergresql docker

### sqlite 3 create table
In this part, I use yfinance to prase stock data and write a database file locally. (reference script [file](sq3_stock.py))

### Pull the postergresql docker and run as container

Reference the previous section (see docker)

### Write db file to container and save as a docker image.

Establish link with local database file is quite easy.
And also quite easy to fetch data.
```python
# SQLite connection
sqlite_conn = sqlite3.connect('stock.db')
# Fetch table names from SQLite
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
```


I use `psycopg2` to establish link to postergresql container.
And write the container with `SQLAlchemy` engine. <br/>
It seems like `psycopg2` is a good connector, however, `SQLAlchemy` is a better writer to interact with SQL software.


```python
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
```

### To parse changes iside the docker image

After connection...

```python
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
```

### Export the container as a docker image
> Following operations are in bash:


You can always check the docker container by:

```bash
docker ps
```

```bash
docker save -o /path/to/directory/mypostgresql-image.tar mypostgresql-image
```
- `mypostgresql-image.tar` is the name of the tar file that will contain your Docker image.
- `mypostgresql-image` is the name of the image you are exporting.

To load docker image

```bash
docker load -i mypostgresql-image.tar
```