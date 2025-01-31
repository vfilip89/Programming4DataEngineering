# TO DO: it only fetches 100 queued flowfiles even if there exist more

import requests

# Set FlowFile queue ID
QUEUE_ID = "bbe49791-0194-1000-f02f-9431cc32f9e1"
BASE_URL = f"http://localhost:9300/nifi-api/flowfile-queues/{QUEUE_ID}"

# Step 1: Start a Listing Request
listing_request = requests.post(f"{BASE_URL}/listing-requests").json()
list_id = listing_request['listingRequest']['id']
print(f"✅ Listing Request ID: {list_id}")

# Step 2: Retrieve FlowFile Listing
LIST_URL = f"{BASE_URL}/listing-requests/{list_id}"
list_response = requests.get(LIST_URL).json()

# Extract FlowFiles
flowfiles = list_response['listingRequest']['flowFileSummaries']
flowfile_count = len(flowfiles)
print(f"\n📌 Total FlowFiles in Queue: {flowfile_count}")

# Handle empty queue case
if not flowfiles:
    print("\n⚠️ No FlowFiles in the queue.")
    # Step 6: Delete the Listing Request
    requests.delete(LIST_URL)
    print("\n✅ Listing request closed.")
    exit()

# Limit display to first 10 FlowFiles if more exist
if flowfile_count > 10:
    print("\n⚠️ More than 10 FlowFiles found. In the sequel displaying info and content for only the first 10.")
    first10flowfiles = flowfiles[:10]

# Display FlowFile details with only ID and Size
print("\n📌 **FlowFiles in Queue:**")
for flowfile in first10flowfiles:
    print(f"🔹 FlowFile ID: {flowfile['uuid']}, Size: {flowfile['size']} bytes")

# Step 3 & 4: Get and Download Content for Each FlowFile
preview_length = 200  # Adjust this value as needed
for flowfile in first10flowfiles:
    ff_id = flowfile['uuid']
    content = requests.get(f"{BASE_URL}/flowfiles/{ff_id}/content").text
    
    print(f"\n📥 FlowFile Content (ID: {ff_id})")
    if len(content) > preview_length * 2:
        print(content[:preview_length] + "\n...\n" + content[-preview_length:])
    else:
        print(content)
    print("\n\n")  # Add two new lines between FlowFiles

# Step 5: Drop the Queue
requests.post(f"{BASE_URL}/drop-requests")
print("\n🗑️ Queue Cleared.")

# Step 6: Delete the Listing Request
requests.delete(LIST_URL)
print("\n✅ Listing request closed.")