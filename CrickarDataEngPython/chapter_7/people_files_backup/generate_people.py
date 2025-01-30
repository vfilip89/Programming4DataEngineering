from faker import Faker
import csv

# Initialize Faker
fake = Faker()

# Define CSV filename and headers
filename = "people.csv"
header = ["name", "age", "street", "city", "state", "zip", "lng", "lat"]

# Generate and write data using "with open"
with open(filename, "w", newline="") as file:
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

print(f"CSV file '{filename}' has been generated successfully!")
