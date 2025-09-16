from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Initial search query with scroll
doc = {
    "query": {"match_all": {}},  # Your query
    "size": 267  # Specify the size in the body
}

# Perform the initial search with scroll
res = es.search(
    index="users",  # The index you are querying
    scroll="20m",  # Scroll timeout (e.g., 20 minutes)
    body=doc  # Pass the query body here
)

# Save the initial scroll ID and size
sid = res['_scroll_id']
size = res['hits']['total']['value']

print("\ntotal size = ",size,"\n")

# Process and print the first batch of results
i = 1
for doc in res['hits']['hits']:
    print(i, doc['_source'])  # Print the index (i) and the document's _source
    i += 1  # Increment the counter

# Start scrolling through the results
while size > 0:
    res = es.scroll(scroll_id=sid, scroll="20m")  # Fetch the next batch of results

    # Update the scroll ID and size
    sid = res['_scroll_id']
    size = len(res['hits']['hits'])
    print("\ncurrent scroll size = ",size,"\n")

    # Process the results (e.g., print the documents)
    i = 1
    for doc in res['hits']['hits']:
        print(i, doc['_source'])  # Print the index (i) and the document's _source
        i += 1  # Increment the counter