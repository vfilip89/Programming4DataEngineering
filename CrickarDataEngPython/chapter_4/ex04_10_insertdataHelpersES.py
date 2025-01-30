from elasticsearch import Elasticsearch, helpers
from faker import Faker

# Create Faker object to generate random data
fake = Faker()

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Prepare actions for bulk insert without '_type'
actions = [
    {
        "_index": "users",
        "_source": {  # '_source' contains the document data
            "name": fake.name(),
            "street": fake.street_address(),
            "city": fake.city(),
            "zip": fake.zipcode()
        }
    }
    for x in range(998)  # Number of records to insert
]

# Perform bulk insert
res = helpers.bulk(es, actions)

# Check result
print(f"Bulk insert result: {res}")