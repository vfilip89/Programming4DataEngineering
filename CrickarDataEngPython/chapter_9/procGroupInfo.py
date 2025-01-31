import requests

# Use your actual Process Group ID
PROCESS_GROUP_ID = "d593c465-0193-1000-1b9c-26c35e39935d"
NIFI_API_URL = f"http://localhost:9300/nifi-api/process-groups/{PROCESS_GROUP_ID}"

# Make API request
response = requests.get(NIFI_API_URL)
pgdata = response.json()

# Extract processor group name and queue information
pg_name = pgdata['component']['name']
queued_flowfiles = pgdata['status']['aggregateSnapshot']['flowFilesQueued']
queued_size = pgdata['status']['aggregateSnapshot']['queuedSize']

# Display information
print(f"📌 Processor Group Name: {pg_name}")
print(f"📊 FlowFiles Queued: {queued_flowfiles}")
print(f"📂 Queued Size: {queued_size}")
