from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",
    group_id="manual_commit_group",  # ✅ Consumer group to track offsets
    auto_offset_reset="earliest",  # ✅ Normally starts at the beginning, but overridden by seek()
    enable_auto_commit=False  # ❌ Do not auto-commit offsets (we control it)
)

# ✅ Manually assign the consumer to a specific partition
partition = TopicPartition("test_topic", 0)
consumer.assign([partition])  # ✅ Assign to partition 0

# ✅ Set the offset to 5 (skipping first 5 messages)
consumer.seek(partition, 5)

# ✅ Read messages from offset 5 onwards
for message in consumer:
    print(f"🟢 Received: {message.value.decode('utf-8')}")
