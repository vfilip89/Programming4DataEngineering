import findspark
findspark.init()
import time
import random
import numpy as np
import multiprocessing
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

def inside(_):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

# 1. Spark-based Monte Carlo Pi estimation
def estimate_pi_spark(num_samples):
    start_time = time.time()
    # .master('spark://localhost:7077')
    spark = SparkSession.builder.appName('Pi-Estimation').getOrCreate()
    count = spark.sparkContext.parallelize(range(num_samples)).filter(inside).count()
    pi_estimate = 4.0 * count / num_samples
    elapsed_time = time.time() - start_time
    spark.stop()
    
    return pi_estimate, elapsed_time

# 2. Serial Python Monte Carlo Pi estimation
def estimate_pi_serial(num_samples):
    start_time = time.time()
    count = sum(1 for _ in range(num_samples) if random.random()**2 + random.random()**2 < 1)
    pi_estimate = 4.0 * count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# 3. Multiprocessing-based Monte Carlo Pi estimation
def estimate_pi_multiprocessing(num_samples, chunk_size=100_000_000):
    start_time = time.time()
    if num_samples <= 100_000_000:  # If small enough, process all at once
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            total_count = sum(pool.map(inside, range(num_samples)))  # Parallel computation
    else:
        total_count = 0
        num_chunks = num_samples // chunk_size  # Calculate the number of chunks
        remainder = num_samples % chunk_size  # Handle leftover samplesotal_count = 0
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            # Process samples in chunks
            for _ in range(num_chunks):
                total_count += sum(pool.map(inside, range(chunk_size)))
            # Process the remainder (if any)
            if remainder > 0:
                total_count += sum(pool.map(inside, range(remainder)))   
    pi_estimate = 4.0 * total_count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# 4. NumPy vectorized Monte Carlo Pi estimation
def estimate_pi_numpy(num_samples, chunk_size=100_000_000):
    start_time = time.time()
    if num_samples <= 100_000_000:  # If small enough, process all at once
        x, y = np.random.random(num_samples), np.random.random(num_samples)
        total_count = np.sum(x**2 + y**2 < 1)
    else:
        total_count = 0
        num_chunks = num_samples // chunk_size  # Calculate number of chunks
        remainder = num_samples % chunk_size  # Handle leftover samples
        for _ in range(num_chunks):
            x, y = np.random.random(chunk_size), np.random.random(chunk_size)
            total_count += np.sum(x**2 + y**2 < 1)
        if remainder > 0:
            x, y = np.random.random(remainder), np.random.random(remainder)
            total_count += np.sum(x**2 + y**2 < 1)
    pi_estimate = 4.0 * total_count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# Benchmarking and Plotting
sample_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000, 1_000_000_000, 5_000_000_000, 10_000_000_000]
# sample_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000, 1_000_000_000][::-1]
spark_times, serial_times, mp_times, numpy_times = [], [], [], []

for num_samples in sample_sizes:
    print(f"\nRunning benchmarks for {num_samples} samples...")
    print(f"Running Spark...")
    pi_spark, time_spark = estimate_pi_spark(num_samples)
    print(f"(Spark) Estimated Pi: {pi_spark:.8f} | Time: {time_spark:.4f}s")
    print(f"Running Serial Python...")
    pi_serial, time_serial = estimate_pi_serial(num_samples)
    print(f"(Serial) Estimated Pi: {pi_serial:.8f} | Time: {time_serial:.4f}s")
    print(f"Running Multiprocessing Python...")
    pi_mp, time_mp = estimate_pi_multiprocessing(num_samples)
    print(f"(Multiprocessing) Estimated Pi: {pi_mp:.8f} | Time: {time_mp:.4f}s")
    print(f"Running Vectorised Python (NumPy)...")
    pi_numpy, time_numpy = estimate_pi_numpy(num_samples)
    print(f"(NumPy) Estimated Pi: {pi_numpy:.8f} | Time: {time_numpy:.4f}s")

    spark_times.append(time_spark)
    serial_times.append(time_serial)
    mp_times.append(time_mp)
    numpy_times.append(time_numpy)

# Plotting results
plt.figure(figsize=(8, 5))
plt.plot(sample_sizes, spark_times, marker='o', linestyle='-', label="Spark")
plt.plot(sample_sizes, serial_times, marker='s', linestyle='-', label="Serial Python")
plt.plot(sample_sizes, mp_times, marker='^', linestyle='-', label="Multiprocessing")
plt.plot(sample_sizes, numpy_times, marker='d', linestyle='-', label="NumPy Vectorized")

plt.xlabel("Number of Samples")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs. Number of Samples (Monte Carlo Pi Estimation)")
plt.xscale("log")  # Log scale for better visualization
plt.grid(True)
plt.legend()
plt.show()
