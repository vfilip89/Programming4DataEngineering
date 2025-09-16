import findspark
findspark.init()
from pyspark.sql import SparkSession
import random

spark = SparkSession.builder \
    .master('spark://localhost:7077') \
    .appName('Pi-Estimation') \
    .getOrCreate()

NUM_SAMPLES = 1000000  # Number of random points to sample

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)) \
        .filter(inside).count()
print('Pi is roughly {}'.format(4.0 * count / NUM_SAMPLES))
