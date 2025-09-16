import psycopg2 as db
import pandas as pd

try:
    # Step 1: Set up the connection
    conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"
    conn = db.connect(conn_string)
    print("Connection established!")

    # Step 2: Execute query and load data into a DataFrame
    query = "SELECT * FROM users"
    df = pd.read_sql(query, conn)
    print("Data loaded into DataFrame!")
    
    # Step 3: Work with the DataFrame
    print("\nPreview of the first 5 rows of the DataFrame:")
    print(df.head())  # Display the first 5 rows
    
    # Export to JSON and save to file
    json_file = "users_data.json"
    df.to_json(json_file, orient='records', indent=4) #If file size matters (e.g., in production or when transferring large data files), skip indentation to save space.
    print(f"\nData exported to JSON file: {json_file}")
    
    # Export to CSV
    csv_file = "users_data.csv"
    df.to_csv(csv_file, index=False)
    print(f"\nData exported to CSV file: {csv_file}")
    
    # Basic analysis
    print("\nSummary statistics:")
    print(df.describe())
    print("\nFrequency of each city:")
    print(df['city'].value_counts())

except Exception as e:
    print("An error occurred:", e)

finally:
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
