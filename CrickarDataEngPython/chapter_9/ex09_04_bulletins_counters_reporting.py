import requests
import json

# Step 1: Read NiFi Bulletin Board (System Messages & Errors)
bulletin_response = requests.get("http://localhost:9300/nifi-api/flow/bulletin-board").json()
bulletins = bulletin_response.get('bulletinBoard', {}).get('bulletins', [])
print("\n📢 **NiFi Bulletin Board Messages:**")
if bulletins:
    for bulletin in bulletins:
        print(f"🔔 [{bulletin['bulletin']['level']}] {bulletin['bulletin']['sourceName']}: {bulletin['bulletin']['message']}")
else:
    print("✅ No bulletins found.")

# Step 2: Read NiFi Counters
counters_response = requests.get("http://localhost:9300/nifi-api/counters").json()
counters = counters_response.get('counters', {}).get('aggregateSnapshot', {}).get('counters', [])
print("\n📊 **NiFi Counters:**")
if counters:
    for counter in counters:
        print(f"🔢 {counter['name']}: {counter['value']}")
else:
    print("✅ No counters found.")

# Step 3: Read Reporting Task Information
REPORTING_TASK_ID = "bbf0937b-0194-1000-7991-d873b86c5e6d"  # Replace with actual task ID
reporting_task_response = requests.get(f"http://localhost:9300/nifi-api/reporting-tasks/{REPORTING_TASK_ID}").json()
reporting_task = reporting_task_response.get('component', {})
print("\n📡 **Reporting Task Status:**")
print(f"🔍 Name: {reporting_task.get('name', 'Unknown')}")
print(f"⚙️ State: {reporting_task.get('state', 'Unknown')}")
print(f"⏳ Run Schedule: {reporting_task.get('schedulingPeriod', 'Unknown')}")
print(f"📅 Scheduling Strategy: {reporting_task.get('schedulingStrategy', 'Unknown')}")

reporting_task_bulletins = reporting_task_response.get('bulletins', {})
if reporting_task_bulletins:
    print("\n📢 **Additional Reporting Task Messages:**")
    for bulletin in reporting_task_bulletins:
        print(f"🔔 [{bulletin['bulletin']['level']}] {bulletin['bulletin']['sourceName']}: {bulletin['bulletin']['message']}")


# Step 4: Save Reporting Task Information to a JSON File
with open("reporting_task.json", "w") as json_file:
    json.dump(reporting_task_response, json_file, indent=4)
print("\n💾 Reporting task information saved to 'reporting_task.json'.")