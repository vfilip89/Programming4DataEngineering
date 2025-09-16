# Project: Working with Databases — PostgreSQL & Elasticsearch via Python, pandas, Airflow & NiFi (Mini Projects)

## Overview
This folder contains **portfolio-ready mini projects** that show how to connect to **PostgreSQL**, load/extract data efficiently with **psycopg2** and **pandas**, and work with **Elasticsearch** (single docs, bulk helpers, search, and scroll). It also includes a small **Airflow DAG** that moves data from PostgreSQL to Elasticsearch. The examples mirror real patterns you’ll reuse in larger pipelines and productionized flows.

---

## Architecture
**What’s covered:**
1. **Relational DB (PostgreSQL) — Python**
   - Create connections with `psycopg2` (connection string, cursor lifecycle)
   - Insert single & multiple rows (`execute`, `executemany`)
   - Extract data (cursor iteration, `fetch*`, `copy_to` CSV dump)

2. **Relational DB — pandas**
   - `pd.read_sql(...)` from PostgreSQL
   - Export DataFrames to CSV/JSON for downstream systems

3. **NoSQL (Elasticsearch) — Python**
   - Insert single documents with `Elasticsearch.index(...)`
   - Bulk indexing with `elasticsearch.helpers.bulk(...)`
   - Queries: `match_all`, `match`, Lucene `q=...`
   - **Scroll API** for >10k results (pagination at scale)

4. **Orchestration — Airflow DAG**
   - Task 1: query PostgreSQL → write CSV
   - Task 2: read CSV → insert into Elasticsearch

5. **(NiFi parity)**
   - Equivalent NiFi processors (ExecuteSQLRecord → SplitText → PutElasticsearchHttp) for low‑code teams

---

## Repository Structure
```
A01_Working_with_Databases/
├── ex04_01_connect2db.py                 # Connect to PostgreSQL (psycopg2)
├── ex04_02_insertdata2db.py              # Insert a single record
├── ex04_03_insertMultipleRecs2db.py      # Bulk insert with executemany
├── ex04_04_extractdataDb.py              # Extract with cursor, fetch*, copy_to
├── ex04_05_extractdataDbDf.py            # Extract with pandas read_sql
├── ex04_08_verifyElasticsearch.py        # Verify ES connectivity/version
├── ex04_09_insertdataES.py               # Insert single documents into ES
├── ex04_10_insertdataHelpersES.py        # Bulk insert into ES with helpers.bulk
├── ex04_11_queryES.py                    # Query ES (match_all, match, Lucene q=)
├── ex04_12_scrollES.py                   # Scroll API to page through large results
├── ex04_13_fromPostgreSQL2ES_dag.py      # Airflow DAG: PostgreSQL → CSV → Elasticsearch
├── fromdb.csv                            # CSV exported from PostgreSQL (copy_to)
├── fromdf.csv                            # CSV exported from pandas DataFrame
├── README_Library_Description.md         # Additional notes (original)
├── users_data.csv                        # Sample relational data
└── users_data.json                       # Sample JSON (for ES demos)
```

---

## Key Features
- **End‑to‑end DB patterns:** connect, insert (single/bulk), extract, transform.  
- **Production‑minded techniques:** single transaction commits, bulk operations, cursor management.  
- **Elasticsearch at scale:** bulk helpers & scroll to overcome the 10k search window.  
- **Airflow orchestration:** atomic, two‑task DAG separating extract and load for easier debugging.  
- **Reproducible artifacts:** sample CSV/JSON outputs for quick verification.

> **Note on idempotency**  
> The simple examples are intentionally transparent; production pipelines should use **ids/upserts** (ES `_id`, SQL UPSERT/MERGE) to avoid duplicate loads across runs.

---

## Skills & Tools Demonstrated
- **Python libraries:** `psycopg2`, `pandas`, `elasticsearch`, `elasticsearch.helpers`  
- **Databases:** PostgreSQL (DDL/DML basics, JDBC concepts), Elasticsearch (indexing, query DSL, Lucene syntax, scroll)  
- **Airflow:** DAG authoring, task dependency, scheduling, logs & observability  
- **Data Engineering:** batch extract/load, CSV dumps, JSON document handling, bulk APIs

---

## Example Use Cases
- Migrate a relational slice (SELECT) to a search index for analytics/ops.  
- Backfill large datasets from PostgreSQL to Elasticsearch with the **scroll + bulk** pattern.  
- Build a minimal EL pipeline (PostgreSQL → CSV → Elasticsearch) with Airflow in <50 LOC.

---

## How to Run (quick starts)
- **PostgreSQL demos**  
  ```bash
  python3 ex04_01_connect2db.py
  python3 ex04_02_insertdata2db.py
  python3 ex04_03_insertMultipleRecs2db.py
  python3 ex04_04_extractdataDb.py
  python3 ex04_05_extractdataDbDf.py
  ```
- **Elasticsearch demos**  
  ```bash
  python3 ex04_08_verifyElasticsearch.py
  python3 ex04_09_insertdataES.py
  python3 ex04_10_insertdataHelpersES.py
  python3 ex04_11_queryES.py
  python3 ex04_12_scrollES.py
  ```
- **Airflow DAG**  
  Copy `ex04_13_fromPostgreSQL2ES_dag.py` to your `$AIRFLOW_HOME/dags`, then:
  ```bash
  airflow webserver &
  airflow scheduler &
  # open http://localhost:8080 and trigger the DAG
  ```

---

## Next Steps
- Add **UPSERT/MERGE** patterns (PostgreSQL “ON CONFLICT DO UPDATE”, ES `_id` + `op_type=index`/`create`) for idempotency.  
- Parameterize connection strings & table/index names (env vars, config files, or Airflow Variables).  
- Provide **NiFi JSON/XML templates** mirroring the Airflow DAG for low‑code deployments.  
- Containerize with **Docker Compose** (PostgreSQL + pgAdmin + Elasticsearch + Kibana + Airflow) for one‑command local runs.
