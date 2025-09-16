import psycopg2 as db

# Define the connection string
conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"

try:
    # Create a connection
    conn = db.connect(conn_string)
    print("Connection established!")

    # Create a cursor
    cur = conn.cursor()
    print("Cursor created!")

    # You are now connected to the database and ready to execute SQL commands
except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the connection when done
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")

