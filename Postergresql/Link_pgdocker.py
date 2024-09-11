#%%
import psycopg2
from psycopg2 import sql

# Define your connection parameters
connection_params = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': '123',
    'host': 'localhost',  # Use 'localhost' since the container is accessed from the host
    'port': 5432          # Default PostgreSQL port
}

#%%
# Establish link and query tables' name
try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**connection_params)

    # Create a cursor object
    cursor = conn.cursor()

    # query to list all the names in publich schema
    cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    """)

    # Execute the query
    # cursor.execute(query)

    # Fetch all table names
    tables = cursor.fetchall()

    # Print the table names
    print("Tables in the database:")
    for table in tables:
        print(table[0])
except Exception as e:
    print(f"An error occurred: {e}")



#%%
try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**connection_params)

    # Create a cursor object
    cursor = conn.cursor()

    # Example query: Get all rows from a table (replace 'your_table' with your table name)
    query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(' '))
    
    # Execute the query
    cursor.execute(query)

    # Fetch all results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
# %%

# %%
