from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Fire and Forget
producer.send("test_topic", value={"event": "fire_and_forget"})

# Synchronous
future = producer.send("test_topic", value={"event": "sync"})
result = future.get()  # This waits for Kafka to acknowledge
print("✅ Message sent synchronously:", result)

# Asynchronous with Callback
def on_send_success(record_metadata):
    print(f"✅ Sent message to {record_metadata.topic} on partition {record_metadata.partition}")

producer.send("test_topic", value={"event": "async"}).add_callback(on_send_success)

producer.flush()  # Ensure all messages are sent before closing
producer.close()
