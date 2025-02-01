# TO DO: it only fetches 100 queued flowfiles even if there exist more

import requests  # Library for making HTTP requests
import json  # Library for handling JSON data

# Set FlowFile queue ID (specific to the NiFi queue you want to query)
QUEUE_ID = "bbe49791-0194-1000-f02f-9431cc32f9e1"  # Unique identifier for the FlowFile queue in NiFi
BASE_URL = f"http://localhost:9300/nifi-api/flowfile-queues/{QUEUE_ID}"  # Base URL for NiFi FlowFile queue API

# Step 1: Start a Listing Request
listing_request = requests.post(f"{BASE_URL}/listing-requests").json()  # Sends a POST request to list flowfiles
list_id = listing_request['listingRequest']['id']  # Extracts the listing request ID
print(f"✅ Listing Request ID: {list_id}")  # Prints confirmation of listing request initiation

# Save listing request details to a JSON file
with open("listing_request.json", "w") as json_file:
    json.dump(listing_request, json_file, indent=4)
print("💾 Listing request details saved to 'listing_request.json'.")

# Step 2: Retrieve FlowFile Listing
LIST_URL = f"{BASE_URL}/listing-requests/{list_id}"  # URL to fetch the listing request results
list_response = requests.get(LIST_URL).json()  # Fetches the listing details as JSON

# Save listing response details to a JSON file
with open("listing_response.json", "w") as json_file:
    json.dump(list_response, json_file, indent=4)
print("💾 Listing response details saved to 'listing_response.json'.")

# Extract FlowFiles from the response
flowfiles = list_response['listingRequest']['flowFileSummaries']  # List of FlowFiles in the queue

flowfiles_queued_count = list_response['listingRequest']['queueSize']['objectCount']  # Number of FlowFiles in the queue
print(f"\n📌 Total FlowFiles in the Queue: {flowfiles_queued_count}")  # Prints number of FlowFiles queued in the queue

flowfile_count = len(flowfiles)  # Count of FlowFiles retrieved
print(f"\n📌 Total FlowFiles retrieved from the Queue: {flowfile_count}")  # Prints number of FlowFiles retrieved from the queue

# Handle empty queue case
if not flowfiles:
    print("\n⚠️ No FlowFiles in the queue.")  # Prints a message if no FlowFiles are found
    requests.delete(LIST_URL)  # Deletes the listing request to free resources
    print("\n✅ Listing request closed.")  # Confirmation message
    exit()  # Exits the script since no FlowFiles exist

# Limit display to first 10 FlowFiles if more exist
if flowfile_count > 10:
    print("\n⚠️ More than 10 FlowFiles found. In the sequel displaying info and content for only the first 10.")  # Warns user if there are more than 10 FlowFiles
    first10flowfiles = flowfiles[:10]  # Takes only the first 10 FlowFiles for display
else:
    first10flowfiles = flowfiles  # If fewer than 10 FlowFiles exist, use them all

# Display FlowFile details with only ID and Size
print("\n📌 **FlowFiles in Queue:**")
for flowfile in first10flowfiles:
    print(f"🔹 FlowFile ID: {flowfile['uuid']}, Size: {flowfile['size']} bytes")  # Displays FlowFile ID and size

# Step 3 & 4: Get and Download Content for Each FlowFile
preview_length = 200  # Number of characters to display from the beginning and end of each FlowFile content
for flowfile in first10flowfiles:
    ff_id = flowfile['uuid']  # Extracts FlowFile ID
    content = requests.get(f"{BASE_URL}/flowfiles/{ff_id}/content").text  # Fetches FlowFile content as text
    
    print(f"\n📥 FlowFile Content (ID: {ff_id})")  # Prints FlowFile content header
    if len(content) > preview_length * 2:
        print(content[:preview_length] + "\n...\n" + content[-preview_length:])  # Shows only the beginning and end of large content
    else:
        print(content)  # Displays full content if it's small enough
    print("\n\n")  # Adds two new lines between FlowFiles for readability

# Step 5: Drop the Queue (Clears all FlowFiles from the queue)
requests.post(f"{BASE_URL}/drop-requests")  # Sends a request to delete all FlowFiles in the queue
print("\n🗑️ Queue Cleared.")  # Prints confirmation message

# Step 6: Delete the Listing Request (Cleanup after retrieving FlowFile details)
requests.delete(LIST_URL)  # Deletes the listing request so it doesn’t remain in NiFi
print("\n✅ Listing request closed.")  # Prints final confirmation
