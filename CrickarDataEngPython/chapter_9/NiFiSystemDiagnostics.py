import requests

# Define the NiFi API endpoint
NIFI_API_URL = "http://localhost:9300/nifi-api/system-diagnostics"

# Make the GET request
response = requests.get(NIFI_API_URL)

# Convert response to JSON format
data = response.json()

# Extract key system metrics
heap_size = data['systemDiagnostics']['aggregateSnapshot']['maxHeap']
total_threads = data['systemDiagnostics']['aggregateSnapshot']['totalThreads']
heap_utilization = data['systemDiagnostics']['aggregateSnapshot']['heapUtilization']

# Print the extracted information
print(f"🖥️ Max Heap Size: {heap_size}")
print(f"🧵 Total Threads: {total_threads}")
print(f"📊 Heap Utilization: {heap_utilization}")
