from elasticsearch import Elasticsearch
from faker import Faker

# Create Faker object to generate random data
fake = Faker()

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")  # Use your Elasticsearch URL and credentials

# Create a random document using Faker
doc = {
    "name": fake.name(),
    "street": fake.street_address(),
    "city": fake.city(),
    "zip": fake.zipcode()
}

# Insert the document into Elasticsearch index
res = es.index(index="users", body=doc)  # Removed doc_type

# Print the result to confirm success
print(res['result'])  # Expected to print 'created'
