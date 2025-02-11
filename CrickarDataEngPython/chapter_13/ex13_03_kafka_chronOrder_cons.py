from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "test_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,  # Prevent automatic offset commit
    value_deserializer=lambda v: v.decode('utf-8')
)

messages = []
json_messages = 0  # Counter for valid JSON messages
MAX_MESSAGES = 100  # Stop after 100 messages

try:
    for i, msg in enumerate(consumer):
        value = msg.value
        print(f"🔹 Received raw message: {value}")

        try:
            json_value = json.loads(value)

            # ❌ Skip messages without a "timestamp"
            if "timestamp" not in json_value:
                print(f"⚠️ Skipping JSON message without timestamp: {json_value}")
                continue

            messages.append(json_value)
            json_messages += 1
            print(f"✅ JSON message added: {json_value}")

        except json.JSONDecodeError:
            print(f"⚠️ Skipping non-JSON message: {value}")

        # 🛑 Stop consuming after MAX_MESSAGES
        if i + 1 >= MAX_MESSAGES:
            break

        # 🛑 Manual Break Option
        user_input = input("\nPress ENTER to continue or type 'q' to stop consuming and proceed: ")
        if user_input.lower() == "q":
            print("\n🛑 Manual break triggered. Stopping message consumption...\n")
            break  # Exit the loop and continue execution

except KeyboardInterrupt:
    print("\n🛑 Consumer interrupted by user.")

finally:
    print("🔄 Closing Kafka consumer...")
    consumer.close()
    print("✅ Kafka consumer closed successfully.")

# 🔥 DEBUG: Print collected messages before sorting
print(f"\n📌 DEBUG: Collected JSON messages before sorting: {messages}")

# ✅ Sort JSON messages by timestamp and print
if json_messages > 0:
    sorted_messages = sorted(messages, key=lambda x: x["timestamp"])

    print("\n✅ JSON Messages Sorted by Timestamp:")
    for message in sorted_messages:
        print(message)

else:
    print("\n❌ No valid JSON messages found in Kafka topic.")
