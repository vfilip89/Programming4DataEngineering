# Project: Production-Ready Batch Pipeline — Data Lake/Kafka → Staging → Validation → Warehouse (PostgreSQL)

## Overview
This project extends the **production-grade batch pipeline** by adding **Apache Kafka** streaming integration in **KRaft mode (no ZooKeeper)**. Data can enter the system from a local **data lake** (JSON files) or via a **Kafka topic** produced by NiFi. The pipeline uses **Apache NiFi** and **NiFi Registry** to orchestrate: ingest → transform → **staging** → **Great Expectations** validation → **warehouse** (PostgreSQL). Design focuses on **processor‑group modularity, version control, env configurability via the Variable Registry, observability, idempotency, and atomicity**.

---

## Architecture
**Pipeline flow (processor‑group oriented):**
1. **ReadDataLake (Ingest)**  
   - `GetFile` reads JSON from a local data‑lake folder  
   - `EvaluateJsonPath` extracts attributes (`userid`, `name`, `age`, `street`, `city`, `state`, `zip`)  
   - `UpdateCounter` tracks throughput (e.g., `datalakerecordsprocessed`)  
   - Output port → downstream groups

2. **(Optional) ScanLake (Monitoring/Alerting)**  
   - `ScanContent` checks content against a dictionary (e.g., VIPs in `data.txt`)  
   - `PutSlack` notifies on matches  
   - Pass‑through output keeps the main flow unaffected

3. **Kafka Producer (NiFi)**  
   - Input from **ReadDataLake** output port  
   - `ControlRate` simulates streaming (e.g., **1** flowfile **/ minute**)  
   - `PublishKafka` writes to topic **`users`** with brokers `localhost:9092,9093,9094`  
   - **Delivery Guarantee:** *Guarantee Replicated Delivery*  
   - Topic created with **3 partitions** to demonstrate consumer groups

4. **Kafka Consumer (NiFi)**  
   - `ConsumeKafka` reads from **`users`** with brokers `localhost:9092,9093,9094`  
   - Example settings: `Offset=Earliest`, `Group ID=NiFi Consumer`  
   - Add a second `ConsumeKafka` with the **same Group ID** to form a consumer group for parallelism across partitions  
   - (Optional) A second consumer group (e.g., `NiFi Consumer2`) can be added to read the topic independently  
   - `ControlRate` (optional) to throttle historical catch‑up; output port → staging

5. **InsertStaging (Load → Staging)**  
   - `PutSQL` inserts into **`${table}`** (Variable Registry; `staging` in TEST)  
   - JDBC pool to PostgreSQL; **Rollback on Failure = True** for **atomicity**  
   - `UpdateCounter` records inserted (e.g., `InsertedStaging`)  
   - Output port for validation

6. **QueryStaging (Row Count & QC Gate)**  
   - `ExecuteSQLRecord` runs `SELECT COUNT(*) FROM ${table}`  
   - `JsonRecordSetWriter` → `{"count": N}` → `EvaluateJsonPath` → `recordcount`  
   - `RouteOnAttribute` gates promotion (e.g., `${recordcount:ge(1000)}`)

7. **ValidateStaging (Great Expectations)**  
   - External **Great Expectations** suite (e.g., `staging.validation`)  
   - `ExecuteStreamCommand` runs tap script (e.g., `sv.py`) via Python 3; parse output; route on `pass`

8. **InsertWarehouse (Promote to Warehouse)**  
   - `ExecuteSQLRecord` (`SELECT * FROM ${table}` from staging) → `SplitText` → `EvaluateJsonPath`  
   - `PutSQL` inserts into **`${warehouse}`** (Variable Registry; `warehouse` in PROD)  
   - Terminal processor (end of flow)

> **Modes of operation**  
> - **Batch:** Data lake → Staging → Validation → Warehouse.  
> - **Streaming:** Data lake → **Kafka (producer)** → **Kafka (consumer)** → Staging → Validation → Warehouse.

---

## Environments & Config
- **Kafka:** local **KRaft-mode** cluster (no ZooKeeper); topic **`users`** with **3 partitions**  
- **Databases:** PostgreSQL  — `test` and `production` DBs (each with `staging`, `warehouse`)  
- **NiFi**; **NiFi Registry** (bucketed/versioned processor groups)  
- **Variable Registry:** env‑specific bindings (`${table}`, `${warehouse}`, JDBC URLs) scoped per processor group  
- **Data Lake:** JSON generator (`populateDataLake.py`) creates ~1,000 records

> **Atomicity & Idempotency**  
> - **Atomicity:** `PutSQL` with *Rollback on Failure* ensures batch transactions are all‑or‑nothing.  
> - **Idempotency:** safe re‑runs; Kafka consumption uses consumer groups/offsets; staging→warehouse is gated by record counts + validation.

---

## Repository Structure
```
ETL_Kafka_production_deployment_simulation/
├── data.txt
├── nifi_flow_definition/
│   └── ProductionDataPipeline_kafka.json      # Full NiFi flow with Kafka integration (JSON export)
├── nifi_templates/
│   └── kafka_production_data_pipeline.xml     # Template of the Kafka-capable pipeline
├── README_Project_Description.md              # This file
└── staging_scripts/
    ├── validate_nifi_staging.py               # NiFi-focused staging validation helper
    └── validate_staging.py                    # Standalone staging validation script
```

---

## Key Features
- **Dual Ingest Paths:** batch (data lake) and streaming (Kafka) using the same downstream PGs.  
- **KRaft‑Mode Kafka:** modern, ZooKeeper‑free cluster configuration.  
- **Throughput Control:** `ControlRate` to simulate/live-throttle message flow.  
- **Scalable Consumption:** multi‑consumer **group** support aligned to **topic partitions**.  
- **Validation Gates:** record‑count threshold + **Great Expectations** suite before promotion.  
- **Transactional Guarantees:** `PutSQL` rollback on failure for **atomicity**.  
- **Versioned, Modular Design:** NiFi Registry + processor‑group reuse.

---

## Skills & Tools Demonstrated
- **Streaming & Batch Orchestration:** Apache NiFi (Publish/ConsumeKafka, ControlRate, RouteOnAttribute)  
- **Kafka (KRaft):** topic design (partitions), consumer groups, offsets, broker lists  
- **Databases:** PostgreSQL (staging/warehouse, JDBC pooling)  
- **Data Quality:** Great Expectations (suite + tap execution)  
- **Automation & Monitoring:** counters, Slack alerts, attribute routing  
- **Python:** Faker data generation; staging validation scripts

---

## Example Use Cases
- Seamlessly switch sources: initial backfill from **data lake**, continuous updates via **Kafka**.  
- Scale consumers to match partitioned throughput; add independent consumer groups for multiple downstreams.  
- Maintain governance: only **validated** data promotes to production warehouse.

---

## Next Steps
- Provide Docker Compose for **NiFi + Kafka (KRaft) + PostgreSQL + pgAdmin + GE**.  
- Use **Python** and **Airflow** orchestration for present project.  
- Extend **Great Expectations** suite (null checks, value ranges, referential integrity).  