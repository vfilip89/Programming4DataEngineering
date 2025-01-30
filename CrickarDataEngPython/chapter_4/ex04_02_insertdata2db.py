import psycopg2 as db

# Define the connection string
conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"

try:
    # Connect to the database
    conn = db.connect(conn_string)
    print("Connection established!")

    # Create a cursor
    cur = conn.cursor()
    print("Cursor created!")

    # Define the query and data
    query2 = "insert into users (id, name, street, city, zip) values(%s, %s, %s, %s, %s)"
    data = (1, 'Big Bird', 'Sesame Street', 'Fakeville', '12345')

    # Check the query with mogrify
    print("Formatted query:", cur.mogrify(query2, data))

    # Execute the query
    cur.execute(query2, data)
    print("Data inserted!")

    # Commit the transaction
    conn.commit()
    print("Transaction committed!")

except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the connection
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")