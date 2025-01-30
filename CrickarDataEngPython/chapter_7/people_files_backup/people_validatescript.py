import great_expectations as gx

# Load Great Expectations Context
context = gx.get_context()

# Run the checkpoint
checkpoint_name = "people_checkpoint"
results = context.run_checkpoint(checkpoint_name=checkpoint_name)

# Print validation results
if results["success"]:
    print("Validation Succeeded!")
else:
    print("Validation Failed!")
