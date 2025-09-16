import great_expectations as gx
import pandas as pd
from great_expectations.core.batch import RuntimeBatchRequest

# Initialize Great Expectations context
context = gx.get_context()

# Define the expectation suite name
expectation_suite_name = "people.validate"

# Load the CSV file as a Pandas DataFrame
df = pd.read_csv("people.csv")

# Define datasource name and data connector name
datasource_name = "people_datasource"
data_connector_name = "default_runtime_data_connector_name"
data_asset_name = "people_asset"

# Add the Pandas datasource if it doesn't already exist
if datasource_name not in [ds["name"] for ds in context.list_datasources()]:
    context.sources.add_pandas(name=datasource_name)

# Create a RuntimeBatchRequest
batch_request = RuntimeBatchRequest(
    datasource_name=datasource_name,
    data_connector_name=data_connector_name,
    data_asset_name=data_asset_name,
    runtime_parameters={"batch_data": df},  # Pass the DataFrame directly
    batch_identifiers={"default_identifier_name": "default"},
)

# Create the validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)

# Run validation
validation_result = validator.validate()

# Save the expectation suite and build Data Docs
context.save_expectation_suite(validator.expectation_suite)
context.build_data_docs()

print("Validation complete! View results in Data Docs.")
