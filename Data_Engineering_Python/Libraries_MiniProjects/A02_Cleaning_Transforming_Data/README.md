# A02 – Cleaning, Transforming, and Enriching Data

This mini‑project collection demonstrates core **data cleaning and transformation techniques** in Python, following Chapter 5 of *Data Engineering with Python* by Paul Crickard.  
It uses real-world e‑scooter trip data from the City of Albuquerque (2019) to explore, clean, and enrich data, before integrating with **Airflow** for orchestration.

---

## 📂 Repository Structure

```
A02_Cleaning_Transforming_Data/
├── EDA_Crickard_ch5.py              # Exploratory Data Analysis walkthrough
├── ex05_01_exploringData101.py      # Basic data exploration with pandas
├── ex05_02_analyzingData101.py      # Quick statistical analysis & summaries
├── ex05_03_dropRowsColumns.py       # Dropping rows/columns, handling nulls
├── ex05_04_createModifyColumns.py   # Creating and modifying DataFrame columns
├── ex05_05_enrichData.py            # Data enrichment with external geocoding
├── ex05_06_cleanData_dag.py         # Airflow DAG: cleaning + filtering pipeline
├── handle_duration.py               # Parsing and handling duration fields
├── scooter.csv                      # Raw scooter trip dataset (May–July 2019)
├── geocodedstreet.csv               # Geocoded addresses with coordinates
├── README_Library_Description.md    # Documentation file
└── __pycache__/                     # Cached Python bytecode
```

---

## 🔑 Key Features

### 1. Exploratory Data Analysis (EDA)
- Inspect dataset structure, column types, and distributions.  
- Detect anomalies such as null values, inconsistent casing, and datatype mismatches.  
- Tools: **pandas** (`head`, `tail`, `describe`, `value_counts`, slicing, filtering).

### 2. Data Cleaning
- Handle missing values with `dropna()` or `fillna()`.  
- Drop unnecessary rows/columns (`region_id`, invalid trips).  
- Standardize column naming conventions and string casing.  
- Convert object columns (e.g., `started_at`) into proper **datetime** types.

### 3. Data Transformation
- Create and modify new columns (splits, calculated fields, labels).  
- Normalize categorical/text values.  
- Efficient conditional updates using `loc` instead of loops.

### 4. Data Enrichment
- Join external geocoding data (`geocodedstreet.csv`) to add latitude/longitude.  
- Merge/join DataFrames for spatial analysis and visualization readiness.

### 5. Orchestration with Apache Airflow
- **DAG (`ex05_06_cleanData_dag.py`)** automates:  
  1. Cleaning scooter trip data.  
  2. Filtering trips within a specific date range.  
  3. Copying the cleaned subset to target location.  
- Demonstrates orchestration of cleaning & transformation tasks in a production‑like workflow.

---

## 📊 Example Workflow

1. **Run EDA**:  
   ```bash
   python EDA_Crickard_ch5.py
   ```

2. **Clean and enrich dataset**:  
   ```bash
   python ex05_05_enrichData.py
   ```

3. **Run Airflow DAG** (place inside `$AIRFLOW_HOME/dags/`):  
   ```bash
   airflow webserver &
   airflow scheduler &
   ```

4. Validate outputs: cleaned files (`cleanscooter.csv`, `may23-june3.csv`) with enriched coordinates.

---

## 🚀 Skills Demonstrated
- Exploratory Data Analysis (EDA)  
- Data Cleaning & Transformation with **pandas**  
- Handling missing values & null imputation  
- Feature creation and enrichment with external data  
- Workflow orchestration with **Apache Airflow**  

---

## 📌 Next Steps
- Extend DAG with validation using **Great Expectations**.  
- Push cleaned/enriched data into PostgreSQL or Elasticsearch for downstream use.  
- Build dashboards in **Kibana** or **Superset** for visualization.  

