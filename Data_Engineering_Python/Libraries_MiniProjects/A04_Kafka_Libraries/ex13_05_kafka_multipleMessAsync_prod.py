from kafka import KafkaProducer
import json
import functools  # ✅ Import functools for partial()

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# ✅ Callback function for successful message delivery
def on_send_success(record_metadata, message):
    print(f"✅ Sent message: {message}")
    print(f"   🏷  Topic: {record_metadata.topic}")
    print(f"   📌 Partition: {record_metadata.partition}")
    print(f"   📍 Offset: {record_metadata.offset}\n")

# ❌ Callback function for failed message delivery
def on_send_error(excp, message):
    print(f"❌ Failed to send message: {message}")
    print(f"   🔴 Error: {excp}\n")

# Send multiple messages asynchronously
messages = [{"event": f"async-{i}"} for i in range(5)]

for msg in messages:
    future = producer.send("test_topic", value=msg)

    # ✅ Use `functools.partial()` to correctly bind `msg`
    future.add_callback(functools.partial(on_send_success, message=msg))
    future.add_errback(functools.partial(on_send_error, message=msg))

# Flush and close producer
producer.flush()
producer.close()
