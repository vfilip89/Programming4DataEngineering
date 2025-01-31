import requests
import matplotlib
import matplotlib.pyplot as plt

# Set interactive backend for Matplotlib
matplotlib.use('TkAgg')  # Ensure this is set before importing pyplot

# Define NiFi API endpoint
NIFI_API_URL = "http://localhost:9300/nifi-api/system-diagnostics"

# Fetch data from NiFi REST API
response = requests.get(NIFI_API_URL)
data = response.json()

# Extract key system metrics
heap_size = data['systemDiagnostics']['aggregateSnapshot']['maxHeap']
heap_utilization = float(data['systemDiagnostics']['aggregateSnapshot']['heapUtilization'].strip('%'))
total_threads = data['systemDiagnostics']['aggregateSnapshot']['totalThreads']

# Print extracted information
print(f"🖥️ Max Heap Size: {heap_size}")
print(f"📊 Heap Utilization: {heap_utilization}%")
print(f"🧵 Total Threads: {total_threads}")

# Create a bar chart
plt.figure(figsize=(6, 4))
plt.bar(["Heap Utilization (%)", "Total Threads"], [heap_utilization, total_threads], color=['blue', 'red'])
plt.title("NiFi System Metrics")
plt.ylabel("Usage")
plt.show()

# Max Heap Size	
# Max memory allocated to NiFi	
# If NiFi runs out of memory, increase it

# Heap Utilization
# Current NiFi memory usage
# If consistently >85%, optimize NiFi

# Total Threads	83
# Number of active NiFi
# tasks	If >500, NiFi may be overloaded