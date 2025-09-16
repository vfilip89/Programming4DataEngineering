# Project: File I/O Fundamentals — CSV/JSON in Python, pandas & Airflow (Mini Projects)

## Overview
This folder contains **hands-on mini projects** demonstrating core file I/O patterns for data engineering: generating and parsing **CSV/JSON** with **Python** and **pandas**, plus a simple **Apache Airflow DAG** to orchestrate a CSV→JSON conversion pipeline. These exercises are framed as portfolio-ready, reusable snippets that underpin later, larger pipelines (staging/warehouse loads, NiFi flows, Kafka streaming).

---

## Architecture
**What’s covered:**
1. **Python CSV I/O**  
   - Write CSV with Python `csv` module, including headers and robust quoting  
   - Read CSV with `csv.DictReader` for name-based access to fields

2. **pandas DataFrames**  
   - `read_csv` / `to_csv` for efficient tabular operations  
   - Create DataFrames from dictionaries; control schema and output (no index)

3. **Python JSON I/O**  
   - Generate JSON with `json.dump` (Faker-based synthetic data)  
   - Parse JSON with `json.load`, access nested structures

4. **pandas + JSON**  
   - `read_json` / `to_json` including `orient='records'` for pipeline-friendly output  
   - Normalize nested payloads before DataFrame construction

5. **Airflow DAG (CSV → JSON)**  
   - `BashOperator` to signal task start  
   - `PythonOperator` to convert CSV → JSON and log selected fields  
   - Scheduling via `schedule_interval` and `default_args`

---

## Repository Structure
```
A00_Reading_Writing_Files/
├── data.csv                         # Sample CSV (Faker-generated or provided)
├── data.json                        # Sample JSON (records array or normalized)
├── ex03_01_wr.py                    # Write/read CSV using Python csv module
├── ex03_02_pd.py                    # Read/write CSV using pandas
├── ex03_03_json.py                  # Write/read JSON using Python json module
├── ex03_04_pdJson.py                # Read/write JSON using pandas (+ normalization tips)
├── ex03_05_csv_to_json_dag.py       # Airflow DAG: CSV → JSON pipeline
├── example.txt                      # Auxiliary text sample
├── output_columns.json              # Example pandas JSON output (columns orient)
└── output_records.json              # Example pandas JSON output (records orient)
```

---

## Key Features
- **Clean, minimal code examples** you can lift into bigger pipelines.  
- **Faker-powered data generation** for quick, realistic test datasets.  
- **Two JSON orientations** (`columns` vs `records`) to suit different downstream tools.  
- **Airflow orchestration** example to convert CSV → JSON on a schedule.  
- **Reproducible outputs** (`output_columns.json`, `output_records.json`) for unit-style checks.

---

## Skills & Tools Demonstrated
- **Python stdlib:** `csv`, `json`, file context managers (`with open(...)`).  
- **pandas:** DataFrame creation, CSV/JSON I/O, normalization strategies.  
- **Airflow:** DAG authoring, `BashOperator`, `PythonOperator`, scheduling & logs.  
- **Data Engineering Basics:** schema headers, quoting, orientations, reproducible runs.

---

## Example Use Cases
- Prototype file ingestion for a new source, then port logic to NiFi/ETL frameworks.  
- Batch CSV → JSON conversions to feed REST services or document stores.  
- Rapid generation of synthetic datasets for QA, demos, or validation suites.

---

## Next Steps
- Add a **unit test harness** (pytest) to assert row counts, schema, and JSON orientation.  
- Extend the Airflow DAG to push JSON to **S3 / MinIO** and notify via Slack/Email.  
- Provide a NiFi template mirroring the CSV/JSON transformations for low-code teams.  
- Containerize examples with **Docker** for one-command local runs.
