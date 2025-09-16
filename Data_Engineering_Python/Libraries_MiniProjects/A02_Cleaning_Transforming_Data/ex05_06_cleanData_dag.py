import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pandas as pd

# Default arguments for the DAG
default_args = {
    'owner': 'vfilip',  # Your identifier or username
    'start_date': dt.datetime(2025, 1, 17, 13, 50, 0),  # Starting date and time
    'retries': 1,  # Number of retry attempts for failed tasks
    'retry_delay': timedelta(minutes=5),  # Wait time between retries
}

# Function to clean the data
def cleanScooter():
    # Read the dataset
    df = pd.read_csv('/home/vfilip/airflow/dags/scooter.csv')  # Path to the CSV file
    
    # Drop unnecessary columns
    df.drop(columns=['region_id'], inplace=True)
    
    # Convert column names to lowercase
    df.columns = [x.lower() for x in df.columns]
    
    # Convert 'started_at' column to datetime
    df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')
    
    # Save the cleaned data
    df.to_csv('/home/vfilip/airflow/dags/cleanscooter.csv', index=False)

# Function to filter the data
def filterData():
    # Read the cleaned dataset
    df = pd.read_csv('/home/vfilip/airflow/dags/cleanscooter.csv')  # Path to the cleaned CSV file
    
    # Define the date range
    fromd = '2019-05-23'
    tod = '2019-06-03'
    
    # Filter the data
    tofrom = df[(df['started_at'] > fromd) & (df['started_at'] < tod)]
    
    # Save the filtered data
    tofrom.to_csv('/home/vfilip/airflow/dags/may23-june3.csv', index=False)

# Define the DAG
with DAG(
    'CleanDataDAG',  # Updated DAG ID
    default_args=default_args,  # Default arguments for the DAG
    schedule=timedelta(minutes=5),  # Runs every 5 minutes
    catchup=False,  # Prevents backfilling of past runs
) as dag:
    
    # Task 1: Clean the data
    cleanData = PythonOperator(
        task_id='clean',
        python_callable=cleanScooter
    )
    
    # Task 2: Filter the data
    selectData = PythonOperator(
        task_id='filter',
        python_callable=filterData
    )
    
    # Task 3: Copy the file to the desktop
    copyFile = BashOperator(
        task_id='copy',
        bash_command='cp /home/vfilip/airflow/dags/may23-june3.csv /home/vfilip/Desktop'
    )
    
    # Set task dependencies
    cleanData >> selectData >> copyFile
