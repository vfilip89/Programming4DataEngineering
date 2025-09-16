import sys
import json
from great_expectations.core.batch import BatchRequest
from great_expectations.data_context import DataContext

# Initialize Great Expectations context
context = DataContext("/home/vfilip/staging/gx")

# Define expectation suite name
suite_name = "staging.validation"

# Define BatchRequest for staging database
batch_request = BatchRequest(
    datasource_name="staging_datasource",
    data_connector_name="default_configured_data_connector_name",
    data_asset_name="staging"
)

# Get Validator
validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)

# Run validation
results = validator.validate()

# Output validation result as JSON
if not results["success"]:
    print(json.dumps({"result": "fail"}))  # Output failure as JSON
else:
    print(json.dumps({"result": "pass"}))  # Output success as JSON

sys.exit(0)  # Always return 0 to avoid NiFi marking it as failure