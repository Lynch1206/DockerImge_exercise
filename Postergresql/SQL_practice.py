#%% use sqlite3 to create a database
import sqlite3
import pandas as pd

# con = sqlite3.connect(':memory:')
con = sqlite3.connect('mydata.db') # create a database file
query = """CREATE TABLE IF NOT EXISTS sales
            (customer VARCHAR(20), product VARCHAR(20), amount FLOAT, date DATE);"""

con.execute(query)
con.commit()

# Insert a few rows of data into the table
data = [('Richard Lucas', 'Notepad', 2.50, '2014-01-02'),
        ('Jenny Kim', 'Binder', 4.15, '2014-01-15'),
        ('Svetlana Crow', 'Printer', 155.75, '2014-02-03'),
        ('Stephen Randolph', 'Computer', 679.40, '2014-02-20')]
statement = "INSERT INTO sales VALUES(?, ?, ?, ?)"
con.executemany(statement, data)
con.commit()

#%%
# Query the sales table
cursor = con.execute("SELECT * FROM sales")
rows = cursor.fetchall()
row_counter = 0
for row in rows:
    print(row)
    row_counter += 1
print('Number of rows: %d' % (row_counter))
# %%
