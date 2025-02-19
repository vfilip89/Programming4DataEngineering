import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Spark-Kafka-Producer") \
    .master("spark://localhost:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

data = [
    Row(key="1", value="Processed data record 1"),
    Row(key="2", value="Processed data record 2"),
    Row(key="3", value="Processed data record 3"),
]

df = spark.createDataFrame(data)

# Show the data
df.show(truncate=False)

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "processed-data") \
    .save()

print("\n✅ Data written to Kafka successfully!\n")



print("Reading data from Kafka...\n")

kafka_df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "processed-data") \
    .load()

# Convert binary key/value to string
processed_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Show results
processed_df.show(truncate=False)

print("✅ Data read from Kafka successfully!\n")




print("✅ Streaming from Kafka began successfully!\n")

streaming_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "processed-data") \
    .load()

# Convert binary key/value to string
streaming_processed_df = streaming_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Write to console
query = streaming_processed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()



print("✅ Streaming from Kafka stopped successfully!\n")

spark.stop()