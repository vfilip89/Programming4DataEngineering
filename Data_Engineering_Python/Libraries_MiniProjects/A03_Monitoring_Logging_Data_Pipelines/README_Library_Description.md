# Monitoring and Logging Data Pipelines

This project focuses on monitoring and logging data pipelines built with Apache NiFi. 
It demonstrates how to track pipeline performance, identify errors, and collect system-level metrics using NiFi’s built-in tools, processors, and the REST API. The present files utilised the NiFi project "pipeline331_from_restApi_to_kibanaBoard" that can be found in the folder "Hands_on_Projects".

---

## 📂 Project Structure

```
.
├── bulletin_response.json
├── counters_response.json
├── ex09_01_nifiSystemDiagnostics.py
├── ex09_02_procInfo.py
├── ex09_03_listingFlowFiles.py
├── ex09_04_bulletins_counters_reporting.py
├── listing_request.json
├── listing_response.json
├── my_get_every_page_data.json
├── myscf_group_data.json
├── nifi_system_diagnostics_response.json
├── README_Library_Description.md
└── reporting_task.json
```

---

## 📝 Description

The project covers three primary approaches to monitoring NiFi data pipelines:

### 1. Monitoring via NiFi GUI
- **Status Bar**: Displays active threads, queued data, remote process group connectivity, component states, and version control status.
- **Processor Group & Processor Status**: Shows in/out metrics, version info, and bulletins for errors.
- **Bulletin Board**: Central place to view all warnings and errors across pipelines.
- **Counters**: Incremental metrics for tracking flowfile counts across processors.

### 2. Monitoring with NiFi Processors & Reporting Tasks
- **UpdateCounter Processor**: Tracks flowfile counts through specific pipeline points.
- **PutSlack Processor**: Sends alerts directly to Slack when failures occur, customizable with flowfile attributes.
- **Reporting Tasks**: Background monitoring (e.g., `MonitorDiskUsage`) that posts to bulletins or external systems.

### 3. Monitoring with Python & NiFi REST API
Python scripts demonstrate how to query and collect monitoring data programmatically:
- `ex09_01_nifiSystemDiagnostics.py`: Retrieves system diagnostics (heap usage, threads, repository usage).
- `ex09_02_procInfo.py`: Fetches processor group information and status details.
- `ex09_03_listingFlowFiles.py`: Lists flowfiles in queues and retrieves their contents.
- `ex09_04_bulletins_counters_reporting.py`: Accesses bulletins, counters, and reporting task data.

### Example Endpoints
- **System Diagnostics**: `/nifi-api/system-diagnostics`
- **Process Groups**: `/nifi-api/process-groups/{id}`
- **Processors**: `/nifi-api/processors/{id}`
- **FlowFile Queues**: `/nifi-api/flowfile-queues/{id}`
- **Bulletin Board**: `/nifi-api/flow/bulletin-board`
- **Counters**: `/nifi-api/counters`
- **Reporting Tasks**: `/nifi-api/reporting-tasks/{id}`

---

## 🚀 Key Learnings

- Use NiFi’s **GUI** for quick, visual monitoring.
- Leverage **processors** and **reporting tasks** for integrated monitoring and alerting (e.g., Slack).
- Build **custom monitoring tools** with Python and the NiFi REST API to gather diagnostics, track processors, fetch flowfile data, and validate counters.

This project provides a foundation for developing robust monitoring strategies for production data pipelines.
