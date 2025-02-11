from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "test_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",  # Start from beginning
    enable_auto_commit=True,  # Auto-commit offsets
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")
