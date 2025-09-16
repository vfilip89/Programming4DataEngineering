from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send all messages to the same partition by using a fixed key
producer.send("test_topic", key=b"ordering_key", value={"message": "Hello Kafka python"})
producer.send("test_topic", key=b"ordering_key", value={"message": "Kafka is running python"})
producer.send("test_topic", key=b"ordering_key", value={"message": "Kafka is running 2 python"})

producer.flush()
producer.close()
