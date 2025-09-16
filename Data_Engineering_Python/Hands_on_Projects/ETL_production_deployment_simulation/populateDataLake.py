from faker import Faker
import json
import os

# Set the data lake directory
data_lake_path = os.path.expanduser("/home/vfilip/datalake")  # For Linux/macOS
# data_lake_path = "C:\\datalake"  # Uncomment for Windows

# Ensure the directory exists
os.makedirs(data_lake_path, exist_ok=True)
os.chdir(data_lake_path)

# Initialize Faker
fake = Faker()
userid = 1  # Primary Key

# Generate 1,000 JSON files
for i in range(1000):
    name = fake.name()
    fname = f"{name.replace(' ', '-')}_{userid}.json"

    data = {
        "userid": userid,
        "name": name,
        "age": fake.random_int(min=18, max=101, step=1),
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip": fake.zipcode()
    }

    # Write JSON data to a file
    with open(fname, 'w') as output:
        json.dump(data, output, indent=4)

    userid += 1  # Increment userid

print(f"✅ Successfully generated 1,000 JSON files in {data_lake_path}")