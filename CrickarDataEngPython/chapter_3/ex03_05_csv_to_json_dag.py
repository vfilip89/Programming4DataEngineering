import datetime as dt  # Standard Python datetime module
from datetime import timedelta  # For time intervals

# Airflow modules
from airflow import DAG  # Core class for defining workflows
from airflow.operators.bash import BashOperator  # Executes shell commands
from airflow.operators.python import PythonOperator  # Executes Python functions

# Pandas library
import pandas as pd  # For working with CSV and JSON data


# Step 1: Define the Python function
def CSVToJson():
    # Step 1: Read the CSV file
    df = pd.read_csv('/home/vfilip/airflow/dags/data.csv')  # Updated path to the data.csv file

    # Step 2: Print each name from the 'name' column
    for i, r in df.iterrows():
        print(r['name'])

    # Step 3: Write the DataFrame to a JSON file
    df.to_json('/home/vfilip/airflow/dags/fromAirflow.JSON', orient='records')  # Updated output path


# Step 2: Define default arguments for the DAG 
default_args = {
    'owner': 'vfilip',  # Replace with your name or identifier
    'start_date': dt.datetime(2025, 1, 7, 17, 50, 0),  # Today’s date and time
    'retries': 1,  # Number of retry attempts
    'retry_delay': timedelta(minutes=5),  # Wait 5 minutes between retries
}


# Step 3: Create the DAG
with DAG(
    'MyCSVDAG',  # DAG ID
    default_args=default_args,  # Default arguments for the DAG
    schedule=timedelta(minutes=5),  # Runs every 5 minutes
    catchup=False,  # Prevents backfilling
    # Alternatively, you can use a crontab expression:
    # schedule_interval='@daily',  # Runs daily
) as dag:

    # Task 1: Print a message using BashOperator
    print_starting = BashOperator(
        task_id='starting',
        bash_command='echo "I am reading the CSV now....."'
    )

    # Task 2: Execute the CSVToJson function using PythonOperator
    CSVJson = PythonOperator(
        task_id='convertCSVtoJson',
        python_callable=CSVToJson  # The function defined earlier
    )

    # Set task dependencies
    print_starting >> CSVJson