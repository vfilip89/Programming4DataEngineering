from faker import Faker
import json

# Writing JSON
fake = Faker()
alldata = {"records": []}

for _ in range(1000):
    data = {
        "name": fake.name(),
        "age": fake.random_int(min=18, max=80, step=1),
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip": fake.zipcode(),
        "lng": float(fake.longitude()),
        "lat": float(fake.latitude())
    }
    alldata['records'].append(data)

with open('data.json', 'w') as f:
    json.dump(alldata, f)

# Reading JSON
with open('data.json', 'r') as f:
    data = json.load(f)

# Access data
print(data['records'][0])       # First record
print(data['records'][0]['name'])  # Name of the first record
