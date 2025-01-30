import psycopg2 as db
from faker import Faker

# Step 1: Create a Faker object and initialize an array and ID counter
fake = Faker()
data = []
i = 2  # Start ID from 2 since ID 1 is already used for Big Bird

# Step 2: Generate 1,000 fake records
for r in range(1000):
    data.append((i, fake.name(), fake.street_address(),
                 fake.city(), fake.zipcode()))
    i += 1

# Step 3: Convert the list into a tuple of tuples
data_for_db = tuple(data)

# Step 4: Connect to the database
conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"
try:
    conn = db.connect(conn_string)
    cur = conn.cursor()
    print("Connection established!")

    # Step 5: Define the query
    query = "INSERT INTO users (id, name, street, city, zip) VALUES (%s, %s, %s, %s, %s)"

    # Step 6: Use mogrify to inspect the query for a single record
    print("Example query:", cur.mogrify(query, data_for_db[0]).decode("utf-8"))

    # Step 7: Execute the query for all records using executemany
    cur.executemany(query, data_for_db)
    conn.commit()
    print("1,000 records inserted successfully!")

except Exception as e:
    print("An error occurred:", e)

finally:
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
