from confluent_kafka import Consumer

# ✅ Step 1: Create a Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092,localhost:9094,localhost:9096',  # Your brokers in KRaft mode
    'group.id': 'python-consumer',  # Consumer group ID
    'auto.offset.reset': 'latest'  # Start reading from the beginning if no offset is stored
})

# ✅ Step 2: Print available topics and partitions
topics_info = consumer.list_topics().topics
print(f"Available topics: {list(topics_info.keys())}")
print(f"Partitions in test_topic: {topics_info['test_topic'].partitions}")

# ✅ Step 3: Subscribe to the test_topic
consumer.subscribe(['test_topic'])
print("🔄 Subscribed to test_topic. Listening for messages...")

# ✅ Step 4: Read messages in a loop
try:
    while True:
        msg = consumer.poll(1.0)  # Poll Kafka every 1 second

        if msg is None:
            continue  # No message yet, keep polling
        
        if msg.error():
            print(f"❌ Error: {msg.error()}")
            continue
        
        # ✅ Step 5: Decode and process the message
        data = msg.value().decode('utf-8')
        print(f"🟢 Received: {data} from partition {msg.partition()} at offset {msg.offset()}")

except KeyboardInterrupt:
    print("\n⏹️ Stopping consumer...")

finally:
    # ✅ Step 6: Close consumer
    consumer.close()
    print("🔒 Consumer closed.")
