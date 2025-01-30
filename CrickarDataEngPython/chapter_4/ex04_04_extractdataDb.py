import psycopg2 as db

# Step 1: Connect to the database
conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"
try:
    conn = db.connect(conn_string)
    cur = conn.cursor()
    print("Connection established!")

    # Step 2: Define and inspect the SELECT query using mogrify
    query = "SELECT * FROM users"
    print("\nFormatted query (using mogrify):", cur.mogrify(query).decode("utf-8"))

    # Execute the query
    cur.execute(query)

    # Step 3: Fetch and print records
    print("\nAll records:")
    for record in cur: # Cursor as iterable
        print(record)

    # Step 4: Use fetch methods
    cur.execute(query)  # Reset the cursor
    print("\nFirst record (using fetchone):", cur.fetchone())

    cur.execute(query)  # Reset the cursor
    print("\nFirst 5 records (using fetchmany):", cur.fetchmany(5))

    cur.execute(query)  # Reset the cursor
    print("\nTotal records (using fetchall):", cur.fetchall())

    # Step 5: Get metadata
    print("\nTotal rows:", cur.rowcount)
    print("Current row:", cur.rownumber)

    # Step 6: Export data to a CSV file
    with open('fromdb.csv', 'w') as f:
        cur.copy_to(f, 'users', sep=',')
    print("\nData exported to 'fromdb.csv'.")

    # Verify the CSV content
    with open('fromdb.csv', 'r') as f:
        print("\nCSV File Content:\n", f.read())

    # If you want to execute the query only once
    # you can load all data in a tuple named all_records
    cur.execute(query)  # Reset the cursor
    all_records = cur.fetchall()  # Fetch all records at once

    # Example usage
    print("\nFirst record:", all_records[0])  # Access the first record
    print("\nTotal records:", len(all_records))  # Total number of records
    for record in all_records:
        print(record)  # Iterate through all records

except Exception as e:
    print("An error occurred:", e)

finally:
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
