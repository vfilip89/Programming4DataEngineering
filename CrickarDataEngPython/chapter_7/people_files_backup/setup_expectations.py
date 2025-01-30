import great_expectations as gx

# Initialize Great Expectations context
context = gx.get_context()

# Define expectation suite name
expectation_suite_name = "people.validate"

# Check if the expectation suite exists, otherwise create it
try:
    suite = context.get_expectation_suite(expectation_suite_name)
    print(f"Expectation suite '{expectation_suite_name}' already exists.")
except gx.exceptions.DataContextError:
    print(f"Creating new expectation suite: '{expectation_suite_name}'")
    suite = context.add_expectation_suite(expectation_suite_name)

# Save the expectation suite
context.save_expectation_suite(suite)

print(f"Expectation suite '{expectation_suite_name}' configured successfully!")
