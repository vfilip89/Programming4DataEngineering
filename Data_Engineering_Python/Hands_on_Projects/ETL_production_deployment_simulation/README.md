# Project: Production-Ready Batch Pipeline — Data Lake → Staging → Validation → Warehouse (PostgreSQL)

## Overview
This project implements a **production-grade batch data pipeline** using **Apache NiFi** and **NiFi Registry**, targeting **PostgreSQL** as the warehouse. It simulates a data lake with JSON files, loads them into a **staging** table, validates data quality with **Great Expectations**, and promotes validated records into the **warehouse**. The design emphasizes **modularity (processor groups), version control, configurability via the Variable Registry, observability, idempotency, and atomicity**.

---

## Architecture
**Pipeline flow (processor-group oriented):**
1. **ReadDataLake (Ingest)**  
   - `GetFile` reads JSON files from a data-lake folder  
   - `EvaluateJsonPath` extracts fields into attributes (`userid`, `name`, `age`, `street`, `city`, `state`, `zip`)  
   - `UpdateCounter` tracks processed records (e.g., `datalakerecordsprocessed`)  
   - Output port → downstream groups

2. **(Optional) ScanLake (Monitoring/Alerting)**  
   - `ScanContent` checks flowfile content against a dictionary file (e.g., VIP names from `data.txt`)  
   - `PutSlack` notifies when a match is found  
   - Pass-through output keeps the main flow unaffected

3. **InsertStaging (Load → Staging)**  
   - `PutSQL` inserts into **`${table}`** (Variable Registry; **test** uses `staging`)  
   - JDBC connection pool to PostgreSQL; **Rollback on Failure = True** for **atomicity**  
   - `UpdateCounter` tracks inserted rows (e.g., `InsertedStaging`)  
   - Output port for validation

4. **QueryStaging (Row Count & QC Gate)**  
   - `ExecuteSQLRecord` runs `SELECT COUNT(*) FROM ${table}`  
   - `JsonRecordSetWriter` returns `{"count": N}`  
   - `EvaluateJsonPath` → `recordcount`  
   - `RouteOnAttribute` (e.g., `${recordcount:ge(1000)}`) gates promotion

5. **ValidateStaging (Great Expectations)**  
   - External **Great Expectations** suite (e.g., `staging.validation`)  
   - `ExecuteStreamCommand` runs a tap script (e.g., `sv.py`) with Python 3; parse output with `EvaluateJsonPath`  
   - `RouteOnAttribute` routes only when the result starts with `pass`

6. **InsertWarehouse (Promote to Warehouse)**  
   - `ExecuteSQLRecord` (`SELECT * FROM ${table}` from staging) → `SplitText` → `EvaluateJsonPath`  
   - `PutSQL` inserts into **`${warehouse}`** (Variable Registry; **production** uses `warehouse`)  
   - Terminal processor (end of flow)

---

## Environments & Config
- **Databases:** `test` and `production` (each with `staging`, `warehouse`) in **PostgreSQL**  
- **Variable Registry:** binds env-specific values (`${table}`, `${warehouse}`, JDBC URLs) per processor group  
- **Version Control:** all groups versioned in **NiFi Registry** (e.g., bucket `DataLake`)  
- **Data Lake:** local folder populated by a Python/Faker script that generates ~1,000 JSON records

> **Atomicity & Idempotency**  
> - **Atomicity:** `PutSQL` with *Rollback on Failure* ensures batch transactions are all-or-nothing.  
> - **Idempotency:** safe re-runs; promotion is gated by record count and validation suite results.

---

## Repository Structure
```
ETL_production_deployment_simulation/
├── data.txt                             # Dictionary for ScanContent (VIPs, keywords)
├── populateDataLake.py                  # Python/Faker script to generate JSON files (data lake)
└── staging_scripts/
    ├── validate_nifi_staging.py         # NiFi-focused staging validation helper
    └── validate_staging.py              # Standalone staging validation script
```
> Note: NiFi flow(s) and processor-group exports (JSON/XML) are versioned in **NiFi Registry** and can be exported alongside this directory as needed.

---

## Key Features
- **Processor-Group Modularity:** reusable ingest, monitoring, staging, validation, and promotion groups.  
- **Variable Registry-Driven Deployments:** switch **TEST** ↔ **PRODUCTION** by changing scoped variables.  
- **Observability:** `UpdateCounter` processors for end-to-end throughput visibility.  
- **Quality Gates:** record-count thresholds + **Great Expectations** data validation before promotion.  
- **Transactional Guarantees:** `PutSQL` with rollback ensures **atomicity**.  

---

## Skills & Tools Demonstrated
- **Orchestration & Flow Design:** Apache NiFi, NiFi Registry  
- **Databases:** PostgreSQL (staging/warehouse patterns, JDBC pooling)  
- **Data Quality:** Great Expectations (suite + tap execution)  
- **Automation & Monitoring:** Slack notifications, counters, attribute routing  
- **Python:** Faker data generation; validation scripts for staging checks  

---

## Example Use Cases
- Promote curated data from a data lake to a governed warehouse after validation.  
- Add department-specific monitoring (e.g., scan for high-value customers) without duplicating the pipeline.  
- Safely re-run batch promotions using idempotent, gated flows.  

---

## Next Steps
- Use python and  **Airflow** to orchestrate and implement present project.  
- Containerize with **Docker Compose** (NiFi/Python + PostgreSQL + pgAdmin + GE) for one-command setup.  
- Expand **Great Expectations** suites (null checks, value ranges, referential integrity).  
