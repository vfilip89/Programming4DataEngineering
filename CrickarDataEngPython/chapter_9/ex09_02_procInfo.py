import requests

# Use your actual Process Group ID
MYSCF_ID = "8d21c527-0194-1000-5a0d-247c49076e53"
NIFI_API_URL = f"http://localhost:9300/nifi-api/process-groups/{MYSCF_ID}"

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

print()

# Define your processor ID (found in the NiFi UI)
MY_GET_EVERY_PAGE_ID = "85733ca0-67d3-1af6-0edd-78a8dd4e0666"
NIFI_API_URL = f"http://localhost:9300/nifi-api/processors/{MY_GET_EVERY_PAGE_ID}"

# Make API request
response = requests.get(NIFI_API_URL)
pdata = response.json()

# Extract relevant data
processor_name = pdata['component']['name']
processor_status = pdata['status']

# Extract processor stats
bytes_read = processor_status['aggregateSnapshot']['bytesRead']
bytes_written = processor_status['aggregateSnapshot']['bytesWritten']
active_threads = processor_status['aggregateSnapshot']['activeThreadCount']

# Display information
print(f"📌 **Processor Name:** {processor_name}")
print(f"📖 **Bytes Read:** {bytes_read} bytes")
print(f"✍ **Bytes Written:** {bytes_written} bytes")
print(f"🔄 **Active Threads:** {active_threads}")