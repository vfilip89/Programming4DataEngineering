import sys
import json
import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator  # Corrected Import
from great_expectations.data_context import DataContext
from great_expectations.core.batch import BatchRequest

# Define default arguments for the DAG
default_args = {
    'owner': 'vfilip',  # Your identifier or username
    'start_date': dt.datetime(2025, 1, 29, 13, 30, 0),  # Starting date and time
    'retries': 1,  # Number of retry attempts for failed tasks
    'retry_delay': timedelta(minutes=5),  # Wait time between retries
}

# Define the data validation function
def validate_data():
    """Run Great Expectations validation inside Airflow."""
    try:
        # Initialize Great Expectations context
        context = DataContext("/home/vfilip/peoplepipeline/gx")

        # Define Expectation Suite
        suite_name = "people.validate"

        # Define Batch Request
        batch_request = BatchRequest(
            datasource_name="people_datasource",
            data_connector_name="default_inferred_data_connector_name",
            data_asset_name="people.csv",
        )

        # Get Validator
        validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)

        # Run Validation
        results = validator.validate()

        # Print JSON result for logging
        validation_result = {"result": "pass" if results["success"] else "fail"}
        print(json.dumps(validation_result))

        # Raise exception if validation fails
        if not results["success"]:
            raise AirflowException("Validation Failed")

    except Exception as e:
        raise AirflowException(f"Validation task failed: {str(e)}")

# Define the DAG
with DAG(
    "validate_people_dag",
    default_args=default_args,
    schedule=timedelta(minutes=5),  # Runs every 5 minutes
    catchup=False,  # Prevents backfilling of past runs
) as dag:

    # Define Airflow tasks
    validate_task = PythonOperator(
        task_id="validate_people",
        python_callable=validate_data,
    )

    # Define task execution flow
    validate_task  # Standalone task for now, no dependencies