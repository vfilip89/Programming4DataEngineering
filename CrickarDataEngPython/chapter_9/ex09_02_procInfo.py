import requests  # Library for making HTTP requests
import json  # Library for handling JSON data

# Use your actual Process Group ID
MYSCF_ID = "8d21c527-0194-1000-5a0d-247c49076e53"  # Replace with your NiFi Process Group ID
NIFI_API_URL = f"http://localhost:9300/nifi-api/process-groups/{MYSCF_ID}"  # API endpoint for Process Groups

# Make API request to get process group information
response = requests.get(NIFI_API_URL)  # Send GET request to NiFi API
pgdata = response.json()  # Convert API response to a Python dictionary

# Extract processor group name
pg_name = pgdata['component']['name']  # Name of the processor group

# Save process group data to a JSON file using the process group name
pg_filename = f"{pg_name.replace(' ', '_').lower()}_group_data.json"  # Create filename dynamically
with open(pg_filename, "w") as json_file:
    json.dump(pgdata, json_file, indent=4)
print(f"💾 Process group data saved to '{pg_filename}'.")

# Extract queue information
queued_flowfiles = pgdata['status']['aggregateSnapshot']['flowFilesQueued']  # Number of FlowFiles in queue
queued_size = pgdata['status']['aggregateSnapshot']['queuedSize']  # Size of queued FlowFiles

# Display processor group information
print(f"\U0001F4CC Processor Group Name: {pg_name}")  # Prints the name of the processor group
print(f"\U0001F4CA FlowFiles Queued: {queued_flowfiles}")  # Displays the number of FlowFiles in queue
print(f"\U0001F4C2 Queued Size: {queued_size}")  # Displays the size of queued FlowFiles

print()  # Prints a blank line for readability

# Define your processor ID (found in the NiFi UI)
MY_GET_EVERY_PAGE_ID = "85733ca0-67d3-1af6-0edd-78a8dd4e0666"  # Replace with your NiFi Processor ID
NIFI_API_URL = f"http://localhost:9300/nifi-api/processors/{MY_GET_EVERY_PAGE_ID}"  # API endpoint for Processors

# Make API request to get processor information
response = requests.get(NIFI_API_URL)  # Send GET request to NiFi API
pdata = response.json()  # Convert API response to a Python dictionary

# Extract relevant processor information
processor_name = pdata['component']['name']  # Name of the processor
processor_status = pdata['status']  # Processor status details

# Save processor data to a JSON file using the processor name
processor_filename = f"{processor_name.replace(' ', '_').lower()}_data.json"  # Create filename dynamically
with open(processor_filename, "w") as json_file:
    json.dump(pdata, json_file, indent=4)
print(f"💾 Processor data saved to '{processor_filename}'.")

# Extract processor stats
bytes_read = processor_status['aggregateSnapshot']['bytesRead']  # Total bytes read by the processor
bytes_written = processor_status['aggregateSnapshot']['bytesWritten']  # Total bytes written by the processor
active_threads = processor_status['aggregateSnapshot']['activeThreadCount']  # Number of active threads

# Display processor information
print(f"\U0001F4CC **Processor Name:** {processor_name}")  # Prints the name of the processor
print(f"\U0001F4D6 **Bytes Read:** {bytes_read} bytes")  # Displays the number of bytes read
print(f"✍ **Bytes Written:** {bytes_written} bytes")  # Displays the number of bytes written
print(f"\U0001F504 **Active Threads:** {active_threads}")  # Displays the number of active threads