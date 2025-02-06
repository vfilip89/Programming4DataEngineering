import great_expectations as gx
from great_expectations.core.batch import BatchRequest

# Initialize Great Expectations context
context = gx.get_context()

# Define the expectation suite name
expectation_suite_name = "staging.validation"

# Define datasource, connector, and asset names
datasource_name = "staging_datasource"
data_connector_name = "default_configured_data_connector_name"
data_asset_name = "staging"

# Create a BatchRequest for SQL data
batch_request = BatchRequest(
    datasource_name=datasource_name,
    data_connector_name=data_connector_name,
    data_asset_name=data_asset_name,
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