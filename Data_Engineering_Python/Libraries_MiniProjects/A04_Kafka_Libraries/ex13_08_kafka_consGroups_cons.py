from kafka import KafkaConsumer

consumer_group = KafkaConsumer(
    "test_topic",
    bootstrap_servers="localhost:9092",
    group_id="my_consumer_group",  # ✅ Kafka will remember offsets for this group
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

for message in consumer_group:
    print(f"👥 Group Consumer Received from Partition {message.partition}: {message.value.decode('utf-8')}")

# consumer_no_group = KafkaConsumer(
#     "test_topic",
#     bootstrap_servers="localhost:9092",
#     auto_offset_reset="earliest",  # ✅ Starts from the first message every time
#     enable_auto_commit=True
# )

# for message in consumer_no_group:
#     print(f"🔄 No Group Consumer Received from Partition {message.partition}: {message.value.decode('utf-8')}")
