import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator  # Executes Python functions
import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch, helpers


# Step 1: Define the functions outside the DAG

# Function to query data from PostgreSQL
def queryPostgresql():
        conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"
        conn = db.connect(conn_string)
        try:
            df = pd.read_sql("SELECT name, city FROM users", conn)
            df.to_csv('/home/vfilip/airflow/dags/postgresqldata.csv')
            print("-------Data Saved------")
        except Exception as e:
            print("An error occurred while querying PostgreSQL:", e)
        finally:
            if conn:
                conn.close()
                print("PostgreSQL connection closed.")

# Function to insert data into Elasticsearch
def insertElasticsearch():
        es = Elasticsearch("http://localhost:9200")
        df = pd.read_csv('/home/vfilip/airflow/dags/postgresqldata.csv')
        
        # for i, r in df.iterrows():
        #     doc = r.to_json()
        #     res = es.index(index="frompostgresql", body=doc)
        #     print(res)

        # Prepare actions for bulk insert
        actions = []
        for i, r in df.iterrows():
            action = {
                "_index": "frompostgresql",  # The index name
                "_source": r.to_dict(),  # The document data
            }
            actions.append(action)
        
        # Perform the bulk insert using the helpers.bulk function
        if actions:
            success, failed = helpers.bulk(es, actions)
            print(f"Successfully indexed {success} documents, failed {failed} documents.")
        else:
            print("No data to insert.")


# Step 2: Define default arguments for the DAG 
default_args = {
    'owner': 'vfilip',  # Replace with your name or identifier
    'start_date': dt.datetime(2025, 1, 16, 10, 45, 0),  # Updated date and time (January 16, 2025)
    'retries': 1,  # Number of retry attempts
    'retry_delay': timedelta(minutes=5),  # Wait 5 minutes between retries
}


# Step 3: Create the DAG
with DAG(
    'MyDBdag',  # DAG ID
    default_args=default_args,  # Default arguments for the DAG
    schedule=timedelta(minutes=5),  # Runs every 5 minutes
    catchup=False,  # Prevents backfilling
    # Alternatively, you can use a crontab expression:
    # schedule_interval='@daily',  # Runs daily
) as dag:

    # Task 1: Query PostgreSQL and save to CSV
    getData = PythonOperator(
        task_id='QueryPostgreSQL',
        python_callable=queryPostgresql
    )

    # Task 2: Insert data from CSV into Elasticsearch
    insertData = PythonOperator(
        task_id='InsertDataElasticsearch',
        python_callable=insertElasticsearch
    )

    # Set task dependencies
    getData >> insertData