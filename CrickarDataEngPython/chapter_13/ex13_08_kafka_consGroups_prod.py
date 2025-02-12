from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: v.encode('utf-8')
)

# ✅ Send a message to Partition 1
producer.send("test_topic", value="2nd New Message for Partition 0", partition=0)
producer.send("test_topic", value="2nd New Message for Partition 1", partition=1)
producer.send("test_topic", value="2nd New Message for Partition 2", partition=2)
producer.send("test_topic", value="New Message for Partition ?")



# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     key_serializer=lambda k: k.encode('utf-8') if k else None,  # Convert key to bytes
#     value_serializer=lambda v: v.encode('utf-8')  # Convert value to bytes
# )

# # ✅ Send messages with keys
# producer.send("test_topic", key="user1", value="2nd Hello from user1")
# producer.send("test_topic", key="user2", value="2nd Hello from user2")
# producer.send("test_topic", key="user1", value="2nd Another message from user1")
# producer.send("test_topic", key="user3", value="2nd Hello from user3")
# producer.send("test_topic", key="user3", value="2nd Another message from user3")
# producer.send("test_topic", key="user2", value="2nd Another message from user2")
# producer.send("test_topic", key="user0", value="2nd Hello from user0")
# producer.send("test_topic", key="user0", value="2nd Another message from user0")





producer.flush()  # ✅ Ensure messages are delivered
producer.close()

