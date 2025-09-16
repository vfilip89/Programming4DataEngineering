import sys
import json
from great_expectations.core.batch import BatchRequest
from great_expectations.data_context import DataContext

# Initialize Great Expectations context
context = DataContext("/home/vfilip/peoplepipeline/gx")

# Define expectation suite name
suite_name = "people.validate"

# Corrected BatchRequest
batch_request = BatchRequest(
    datasource_name="people_datasource",  
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="people.csv"
)

# Get Validator
validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)

# Run validation
results = validator.validate()

# Check if validation passed or failed
if not results["success"]:
    print(json.dumps({"result": "fail"}))  # Print JSON output for NiFi
    sys.exit(0)

print(json.dumps({"result": "pass"}))  # Print JSON output for NiFi
sys.exit(0)
