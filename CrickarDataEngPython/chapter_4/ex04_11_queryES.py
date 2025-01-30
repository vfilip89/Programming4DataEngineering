from elasticsearch import Elasticsearch
from pandas import json_normalize

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Match all query to fetch all records
doc = {
    "query": {
        "match_all": {}
    },
    "size": 10  # Specify the size in the body to avoid deprecation warning
}

# Perform the search operation
res = es.search(index="users", body=doc)

# Print all documents
print("\n",res['hits']['hits'],"\n")

# Print the _source field (the actual data)
for doc in res['hits']['hits']:
    print(doc['_source'])

# Load results into DataFrame
df = json_normalize(res['hits']['hits'])
print("\n",df.head())

# Extract the _source field and normalize it
data = [doc['_source'] for doc in res['hits']['hits']]
# Normalize the _source data into a DataFrame
df0 = json_normalize(data)
print("\n",df0.head(),"\n")


# Query for documents where name matches "Ronald Goodman"
doc2 = {
    "query": {
        "match": {
            "name": "Pamela Matthews"
        }
    },
    "size": 10  # Specify the size in the body
}

# Perform the search operation
res2 = es.search(index="users", body=doc2)

# Extract and normalize only the _source field
data2 = [doc2['_source'] for doc2 in res2['hits']['hits']]
df2 = json_normalize(data2)
print("\n",df2.head(),"\n")


# Query for exact match of "Pamela Matthews"
doc3 = {
    "query": {
        "match_phrase": {
            "name": "Pamela Matthews"
        }
    },
    "size": 10  # Specify the size in the body
}
res3 = es.search(index="users", body=doc3)
data3 = [doc3['_source'] for doc3 in res3['hits']['hits']]
df3 = json_normalize(data3)
print("\n",df3.head(),"\n")


# Perform a Lucene search for name: "Ronald Goodman"
res4 = es.search(index="users", q='name:"Pamela Matthews"', size=10)
data4 = [doc4['_source'] for doc4 in res4['hits']['hits']]
df4 = json_normalize(data4)
print("\n",df4.head(),"\n")


# Query for city "Jamesberg"
doc5 = {
    "query": {
        "match": {
            "city": "Port"
        }
    },
    "size": 10  # Specify the size in the body
}
res5 = es.search(index="users", body=doc5)
data5 = [doc5['_source'] for doc5 in res5['hits']['hits']]
df5 = json_normalize(data5)
print("\n",df5.head(),"\n")


# Boolean query to filter by city and zip code
doc6 = {
    "query": {
        "bool": {
            "must": {
                "match": {
                    "city": "Port"
                }
            },
            "filter": {
                "term": {
                    "zip": "20054"
                }
            }
        }
    },
    "size": 10  # Specify the size in the body
}
res6 = es.search(index="users", body=doc6)
data6 = [doc6['_source'] for doc6 in res6['hits']['hits']]
df6 = json_normalize(data6)
print("\n",df6.head(),"\n")


# Lucene query to filter by city and zip code
query = "city:Port AND name:Jonathon"  # Lucene query syntax
res7 = es.search(index="users", q=query, size=10)
data7 = [doc7['_source'] for doc7 in res7['hits']['hits']]
df7 = json_normalize(data7)
print("\n",df7.head(),"\n")