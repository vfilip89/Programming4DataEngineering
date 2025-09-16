from confluent_kafka import Producer
from faker import Faker
import json
import time

# Create Faker instance
fake = Faker()

# Create Kafka producer (adjust brokers for your setup)
p = Producer({'bootstrap.servers': 'localhost:9092,localhost:9094,localhost:9096'})
# p = Producer({'bootstrap.servers': 'localhost:9092'})

#Lists all available Kafka topics the producer can send messages to
# p.list_topics().topics 

# Callback function for acknowledgments
def receipt(err, msg):
    if err is not None:
        print(f"❌ Error: {err}")
    else:
        print(f"✅ {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg.timestamp()[1]/1000))} : "
              f"Message on topic {msg.topic()} on partition {msg.partition()} "
              f"with value {msg.value().decode('utf-8')}")
        print()

# Generate and send 10 fake messages
for i in range(10):
    data = {
        'name': fake.name(),
        'age': fake.random_int(min=18, max=80, step=1),
        'street': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zip': fake.zipcode()
    }

    m = json.dumps(data)  # Convert dict to JSON string

    p.poll(0)  # Check for previous acknowledgments
    p.produce('test_topic', m.encode('utf-8'), callback=receipt)  # Send to Kafka

# Ensure all messages are sent
p.flush()
