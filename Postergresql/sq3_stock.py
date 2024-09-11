#%%
# From https://medium.com/cassandra-cryptoassets/download-and-store-stock-prices-using-python-and-sqlite-e5fa0ea372cc
import pandas as pd
import sqlite3
import yfinance as yf
#%%
# ticker inputs
bt_inputs = {'tickers': ['EQIX', 'SNPS', 'VIG'], 
             'start_date': '2019-01-01', 
             'end_date': '2024-09-10'}

# create a sql connection
con = sqlite3.connect('stock.db')
c = con.cursor()
# create price table
query1 = """CREATE TABLE IF NOT EXISTS prices (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
price REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query1.replace('\n',' '))
# create volume table
query2 = """CREATE TABLE IF NOT EXISTS volume (
Date TEXT NOT NULL,
ticker TEXT NOT NULL,
volume REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query2.replace('\n',' '))

def download(bt_inputs, proxy = None):
    data = yf.download(tickers= bt_inputs['tickers'],
                       start = bt_inputs['start_date'],   
                       end = bt_inputs['end_date'],
                       interval = '1d',
                       prepost = True,
                       threads = True,
                       proxy = proxy)
    return data

test = download(bt_inputs)
# %%
adj_close = test['Adj Close']
volume = test['Volume']
# convert wide to long
adj_close_long = pd.melt(adj_close.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name ="ticker", value_name="price")
volume_long = pd.melt(volume.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "volume")
# Push financial data into the database

adj_close_long.to_sql('prices', con, if_exists='append', index=False)
volume_long.to_sql('volume', con, if_exists='append', index=False)
# %%
