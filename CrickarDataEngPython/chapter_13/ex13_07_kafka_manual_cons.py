from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "test_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False  # You must commit manually
)

for message in consumer:
    print(f"Received: {message.value}")
    consumer.commit()  # Manually commit offset
