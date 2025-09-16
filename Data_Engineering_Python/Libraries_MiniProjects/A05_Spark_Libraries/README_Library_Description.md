# A05 — Apache Spark Libraries (Portfolio)

This folder demonstrates how I use **Apache Spark** (standalone mode) with **PySpark** for batch-style data engineering tasks and a simple publish-to-Kafka hand‑off. The material covers cluster setup, local dev with Jupyter, and PySpark DataFrame operations.

> Note: The Kafka hand‑off example assumes a Kafka **KRaft** (no ZooKeeper) cluster. No NiFi steps are included here.

---

## Folder structure

```
A05_Spark_Libraries/
├── data.csv
├── ex14_01_test_spark.ipynb
├── ex14_01_test_spark.py
├── ex14_02_spark_piCalc_benchmark.py
├── ex14_02_spark_piCalc.ipynb
├── ex14_02_spark_piCalc.py
├── ex14_03_spark_data.py
└── ex14_04_spark_Spark2Kafka.py
```

---

## What this mini‑library shows

- Stand up a local Spark standalone cluster and connect from PySpark.
- Use Jupyter + `findspark` for a smooth dev loop.
- Read, inspect, filter, and aggregate tabular data with Spark DataFrames.
- Estimate π with an RDD compute pattern (and benchmark it).
- Optional: publish processed rows to Kafka (KRaft mode).

---

## Dataset

- `data.csv` — synthetic people data with columns like `name, age, street, city, state, zip, lng, lat`.
