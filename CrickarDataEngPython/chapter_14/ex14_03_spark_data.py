import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
import os

# Ensure you set the correct working directory
os.chdir('/home/vfilip/Documents/data_engineering/Programming4DataEngineering/CrickarDataEngPython/chapter_14')  # Change to match your setup

# Create the Spark session
spark = SparkSession.builder \
    .master('spark://localhost:7077') \
    .appName('DataFrame-Kafka') \
    .getOrCreate()


# Load the CSV file
df = spark.read.csv('data.csv')
# Display the first 5 rows
df.show(5)
# Display the DataFrame schema
df.printSchema()

# Load the CSV file enforcing Schema and Headers
df = spark.read.csv('data.csv', header=True, inferSchema=True)
# Show first 5 rows
df.show(5)
# Display schema
df.printSchema()


# Filtering Data
df.select('name').show()
# True for rows where age is less than 40
df.select(df['age']<40).show()
# Select only rows where age is less than 40
df.filter(df['age'] < 40).show()
# Alternative syntax
df.filter("age < 40").select(["name", "age", "state"]).show()


# Collecting Data
# Get all rows where age < 40
u40 = df.filter("age < 40").collect()
# Print the first row
print(u40[0])
# Print the first element
print(u40[0][0])
# Convert row to dictionary
print(u40[0].asDict())
# Extract specific field
print(u40[0].asDict()['name'])
print()
# for x in u40:
#     print(x.asDict())
print()


# SQL Querying with Spark DataFrames
df.createOrReplaceTempView("people")
df_over40 = spark.sql("SELECT * FROM people WHERE age > 40")
df_over40.show()
print()

# Basic analysis
df.describe("age").show()
df.groupBy("state").count().show()
df.agg({"age": "mean"}).show()
print()
print()

# Using PySpark Functions
import pyspark.sql.functions as f

# # Get unique states
# a=df.select(f.collect_set(df['state'])).collect()
# # Count distinct states
# df.select(f.countDistinct('state').alias('states')).show()
# # Hash function
# df.select(f.md5('street').alias('hash')).collect()
# # Reverse string
# df.select(f.reverse(df.state).alias('state-reverse')).collect()
# returns a soundex of the name field for each row
df.select(f.soundex(df.name).alias('soundex')).collect()


# Show Initial DataFrame
print("✅ Original DataFrame:")
df.show()

# 1️⃣ Get Unique States using collect_set()
df_unique_states = df.select(f.collect_set(df["state"]).alias("unique_states"))
print("✅ Unique States:")
df_unique_states.show(truncate=False)
states = df.select(f.collect_set("state")).collect()[0][0]  # Extract list
print("\n✅ Unique States structured:\n" + ", ".join(states))  # Print them nicely
print("✅ Unique States with distinct:")
df.select("state").distinct().show(truncate=False)

# 2️⃣ Count Distinct States using countDistinct()
df_count_states = df.select(f.countDistinct("state").alias("distinct_state_count"))
print("✅ Count of Unique States:")
df_count_states.show()

# 3️⃣ Hash Function using md5()
df_hashed = df.select("street", f.md5("street").alias("hash"))
print("✅ MD5 Hash of Street Column:")
df_hashed.show(truncate=False)

# 4️⃣ Reverse String using reverse()
df_reversed = df.select("state", f.reverse(df.state).alias("state_reversed"))
print("✅ Reversed State Column:")
df_reversed.show()

# 5️⃣ Soundex Encoding using soundex()
df_soundex = df.select("name", f.soundex(df.name).alias("soundex"))
print("✅ Soundex Encoding of Name Column:")
df_soundex.show()


print()
spark.stop()