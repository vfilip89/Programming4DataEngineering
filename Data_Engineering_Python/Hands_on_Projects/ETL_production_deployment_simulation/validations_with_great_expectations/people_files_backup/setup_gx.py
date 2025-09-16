import great_expectations as gx

# Initialize Great Expectations context
context = gx.get_context()

# Define datasource name
datasource_name = "people_datasource"

# List existing datasources properly
existing_datasources = [ds["name"] for ds in context.list_datasources()]
if datasource_name in existing_datasources:
    print(f"Datasource '{datasource_name}' already exists. Deleting it first...")
    context.delete_datasource(datasource_name)

# Add a new Pandas-based datasource
context.sources.add_pandas(name=datasource_name)

# Save the context
context._save_project_config()

print(f"Datasource '{datasource_name}' configured successfully!")
