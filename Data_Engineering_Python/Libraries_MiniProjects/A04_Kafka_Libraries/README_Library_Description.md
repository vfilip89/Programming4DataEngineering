# Kafka Libraries – Producing & Consuming with Python

This project demonstrates how to work with **Apache Kafka in KRaft mode** (without ZooKeeper) using Python. It covers foundational concepts of Kafka logging, message ordering, partitions, consumer groups, and Python-based producers and consumers. The implementation emphasizes real-time data streaming and monitoring of message flows across partitions.

---

## 📂 Project Structure

```
.
├── ex13_01_simple_log.py
├── ex13_02_kafka_messageSamePart_prod.py
├── ex13_03_kafka_chronOrder_cons.py
├── ex13_03_kafka_chronOrder_prod.py
├── ex13_04_kafka_testProdMethos_prod.py
├── ex13_05_kafka_multipleMessAsync_prod.py
├── ex13_06_kafka_auto_cons.py
├── ex13_07_kafka_manual_cons.py
├── ex13_08_kafka_consGroups_cons.py
├── ex13_08_kafka_consGroups_prod.py
├── ex13_10_kafka_confluent_cons.py
├── ex13_10_kafka_confluent_prod.py
├── python-log.log
└── README_Library_Description.md
```

---

## 📝 Description

The project is structured into incremental examples, showing how to log, produce, and consume Kafka messages with increasing complexity.

### 1. Logging Basics
- `ex13_01_simple_log.py`: Demonstrates structured logging in Python with severity levels and timestamps. Outputs to `python-log.log`.

### 2. Kafka Producers
- `ex13_02_kafka_messageSamePart_prod.py`: Produces messages consistently to the same partition using keys.
- `ex13_03_kafka_chronOrder_prod.py`: Ensures chronological order of messages when producing.
- `ex13_04_kafka_testProdMethos_prod.py`: Tests producer delivery methods (`fire-and-forget`, synchronous, asynchronous).
- `ex13_05_kafka_multipleMessAsync_prod.py`: Sends multiple messages asynchronously for higher throughput.
- `ex13_08_kafka_consGroups_prod.py`: Produces messages for testing consumer group scaling.
- `ex13_10_kafka_confluent_prod.py`: Demonstrates production with the Confluent Kafka Python client.

### 3. Kafka Consumers
- `ex13_03_kafka_chronOrder_cons.py`: Reads messages in chronological order from partitions.
- `ex13_06_kafka_auto_cons.py`: Consumes messages with automatic offset commits.
- `ex13_07_kafka_manual_cons.py`: Consumes messages with manual offset control for reliability.
- `ex13_08_kafka_consGroups_cons.py`: Shows how consumer groups distribute partitions among consumers.
- `ex13_10_kafka_confluent_cons.py`: Demonstrates consumption using the Confluent Kafka Python client.

---

## 🚀 Key Learnings

- **Logs as a foundation**: Kafka topics are immutable, ordered logs of events.
- **Partitions & Keys**: Using keys ensures related messages stay in the same partition, preserving order for that subset of data.
- **Producers**: Support multiple delivery semantics – fire-and-forget, synchronous, asynchronous – balancing performance and reliability.
- **Consumers**: Handle offsets (auto or manual) to guarantee at-least-once or exactly-once delivery semantics.
- **Consumer Groups**: Allow scaling by distributing partitions across multiple consumers, ensuring parallelism while maintaining per-partition order.
- **Confluent Client**: Provides advanced features and optimizations for real-world production pipelines.

This library equips data engineers with the building blocks to create **real-time, Python-driven Kafka pipelines** ready for integration with broader data platforms.
