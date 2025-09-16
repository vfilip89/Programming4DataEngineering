# Project: SeeClickFix 311 Data Pipeline → Elasticsearch → Kibana

## Overview
This project implements a **production-style data pipeline** that ingests open civic data from the [SeeClickFix REST API](https://seeclickfix.com/), processes and enriches it in **Apache NiFi**, stores it in **Elasticsearch**, and visualizes trends and geospatial insights in **Kibana**.  
The goal is to demonstrate **real-world data engineering practices**: API ingestion, transformation, schema mapping, idempotent indexing, and dashboarding for downstream analytics.

---

## Architecture
**Pipeline flow:**
1. **NiFi ingestion**  
   - Scheduled trigger with `GenerateFlowFile`  
   - Groovy scripts (`ExecuteScript`) to query the SeeClickFix API  
   - Automatic pagination (`myGetEveryPage.groovy`)  
   - Backfill strategy for archived data (`myQuerySCFArchive.groovy`)  

2. **Transformation**  
   - Split JSON into individual issues  
   - Enrichment:  
     - Concatenate lat/lng into `coords` (`geo_point`)  
     - Extract `opendate` from `created_at`  
   - Add unique identifier (`id`) for idempotent indexing  

3. **Storage**  
   - Load issues into **Elasticsearch**
   - Monitoring using PgAdmin4  
   - Use `upsert` mode for idempotency (avoiding duplicates)  
   - Apply custom mapping (`coords` as `geo_point`)  

4. **Visualization**  
   - Build a **Kibana dashboard** with:  
     - Time-series of issues (bar chart by month)  
     - Issue counts (metric)  
     - Category distribution (donut chart)  
     - Geospatial visualization (map layer)  
     - Markdown context panel  

---

## Repository Structure
```
pipeline331_from_restApi_to_kibanaBoard/
├── nifi_flow_definition/
│   └── mySCF.json                     # Full NiFi flow definition (JSON export)
├── nifi_processor_scripts/
│   ├── myCoords.groovy                # Adds geo-coordinates & dates
│   ├── myGetEveryPage.groovy          # Handles API pagination recursively
│   ├── myQuerySCF.groovy              # Queries current issues from API
│   └── myQuerySCFArchive.groovy       # Backfill archived issues
└── nifi_templates/
    ├── ex06_01_my_SCF_1page_pipeline.xml
    ├── ex06_02_my_SCF_everypage_pipeline.xml
    ├── ex06_03_my_SCF_everypage_withBackfilling_pipeline.xml
    └── ex06_03_my_SCF_final_pipeline.xml
```

---

## Key Features
- **Groovy scripting in NiFi** (modern replacement for deprecated Jython).
- **Idempotent ingestion** using Elasticsearch `_id` and upsert.  
- **Scalable pagination** via processor self-loops.  
- **Backfill mechanism** for full historical data recovery.  
- **Kibana dashboard** enabling time, category, and geospatial filtering.  

---

## Skills & Tools Demonstrated
- **Data Ingestion**: REST APIs, NiFi processors, Groovy scripting.  
- **Data Transformation**: JSON handling, schema enrichment, geopoint mapping.  
- **Data Storage**: Elasticsearch indexing strategies, schema design.  
- **Data Visualization**: Kibana dashboards for civic data insights.  
- **Pipeline Design**: Idempotency, backfilling, production-ready flow design.  

---

## Example Use Cases
- Monitoring quality-of-life issues (graffiti, potholes, abandoned vehicles).  
- Detecting geospatial patterns in civic complaints.  
- Building a reproducible ETL pipeline for any REST-based open data API.  

---

## Next Steps
- Reproduce that pipeline using Python & Airflow DAGs instead of NiFi
- Containerize the pipeline with Docker Compose: NiFi/Python + Elasticsearch + PgAdmin4 + Kibana.    
- Add data quality checks with Great Expectations.  
