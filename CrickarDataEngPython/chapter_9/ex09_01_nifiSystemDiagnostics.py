import requests  # Library for making HTTP requests
# import matplotlib  # Library for creating static, animated, and interactive visualizations
import matplotlib.pyplot as plt  # Submodule for plotting in Matplotlib
import json  # Library for working with JSON data

# print(matplotlib.get_backend())
# Set interactive backend for Matplotlib
# matplotlib.use('TkAgg')  # Ensures Matplotlib can render the plot in a GUI window

# Define NiFi API endpoint for system diagnostics
NIFI_API_URL = "http://localhost:9300/nifi-api/system-diagnostics"  # URL to fetch system diagnostics from NiFi

# Fetch data from NiFi REST API
response = requests.get(NIFI_API_URL)  # Makes a GET request to the NiFi API
data = response.json()  # Converts the API response into a Python dictionary

# Save full API response data to a JSON file
with open("nifi_system_diagnostics_response.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
print("\n💾 Full NiFi API response saved to 'nifi_full_response.json'.")

# Extract key system metrics from the response data
heap_size = data['systemDiagnostics']['aggregateSnapshot']['maxHeap']  # Maximum memory allocated to NiFi
heap_utilization = float(data['systemDiagnostics']['aggregateSnapshot']['heapUtilization'].strip('%'))  # Memory usage in percentage
total_threads = data['systemDiagnostics']['aggregateSnapshot']['totalThreads']  # Number of active processing threads in NiFi

# Print extracted system metrics to the console
print(f"\U0001F5A5️ Max Heap Size: {heap_size}")  # Displays the max heap size (allocated memory)
print(f"\U0001F4CA Heap Utilization: {heap_utilization}%")  # Shows the percentage of memory being used
print(f"\U0001F9D5 Total Threads: {total_threads}")  # Displays the number of active processing threads

# Create a bar chart to visualize system metrics
plt.figure(figsize=(6, 4))  # Sets the size of the figure (6 inches wide, 4 inches tall)
plt.bar(["Heap Utilization (%)", "Total Threads"], [heap_utilization, total_threads], color=['blue', 'red'])  # Plots a bar chart with system metrics
plt.title("NiFi System Metrics")  # Adds a title to the plot
plt.ylabel("Usage")  # Labels the y-axis as "Usage"
plt.show()  # Displays the plot

# Explanation of Key Metrics:
#
# Max Heap Size: 
# - Maximum memory allocated to NiFi.
# - If NiFi runs out of memory, consider increasing this value.
#
# Heap Utilization:
# - Current NiFi memory usage as a percentage.
# - If consistently >85%, NiFi might need optimization.
#
# Total Threads:
# - Number of active processing tasks in NiFi.
# - If the number exceeds 500, NiFi might be overloaded.
