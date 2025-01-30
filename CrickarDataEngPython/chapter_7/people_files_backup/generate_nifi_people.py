from faker import Faker
import csv
import json
import os

# Initialize Faker
fake = Faker()

# Define CSV filename and headers
output_path = "/home/vfilip/peoplepipeline/people.csv"  # Adjust path for NiFi
header = ["name", "age", "street", "city", "state", "zip", "lng", "lat"]

try:
    # Generate and write data
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header row
        
        # Generate and write 1000 records
        writer.writerows([
            [
                fake.name(),
                # fake.random_int(min=1, max=100, step=1),
                fake.random_int(min=18, max=80, step=1),
                fake.street_address(),
                fake.city(),
                fake.state(),
                fake.zipcode(),
                fake.longitude(),
                fake.latitude()
            ]
            for _ in range(1000)
        ])

    # Output success message in JSON format for NiFi
    print(json.dumps({"status": "Complete"}))

except Exception as e:
    print(json.dumps({"status": "Failed", "error": str(e)}))
