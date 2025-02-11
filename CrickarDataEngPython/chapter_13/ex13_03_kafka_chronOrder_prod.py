import time
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Produce messages with timestamps
producer.send("test_topic", value={"timestamp": time.time(), "message": "Last Hello Kafka python time"})
producer.send("test_topic", value={"timestamp": time.time(), "message": "Last Kafka is running python time"})
producer.send("test_topic", value={"timestamp": time.time(), "message": "Last Kafka is running 3  python time"})

producer.flush()
producer.close()
