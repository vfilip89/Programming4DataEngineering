import findspark
findspark.init()
import time
import random
import numpy as np
import multiprocessing
import dask.array as da
import ray
# from mpi4py import MPI
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import subprocess
import os
from numba import jit, prange
import pandas as pd


# Initialize function for Monte Carlo method
def inside(_):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

# 1. Spark-based Monte Carlo Pi estimation
def estimate_pi_spark(num_samples):
    start_time = time.time()
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
def estimate_pi_multiprocessing(num_samples, chunk_size):
    start_time = time.time()
    if num_samples <= chunk_size:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            total_count = sum(pool.map(inside, range(num_samples)))
    else:
        total_count = 0
        num_chunks = num_samples // chunk_size
        remainder = num_samples % chunk_size
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for _ in range(num_chunks):
                total_count += sum(pool.map(inside, range(chunk_size)))
            if remainder > 0:
                total_count += sum(pool.map(inside, range(remainder)))
    pi_estimate = 4.0 * total_count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# 4. NumPy vectorized Monte Carlo Pi estimation
def estimate_pi_numpy(num_samples, chunk_size):
    start_time = time.time()
    if num_samples <= chunk_size:
        x, y = np.random.random(size=(2, num_samples))
        total_count = np.sum(x**2 + y**2 < 1)
    else:
        total_count = 0
        num_chunks = num_samples // chunk_size
        remainder = num_samples % chunk_size
        for _ in range(num_chunks):
            x, y = np.random.random(size=(2, chunk_size))
            total_count += np.sum(x**2 + y**2 < 1)
        if remainder > 0:
            x, y = np.random.random(size=(2, remainder))
            total_count += np.sum(x**2 + y**2 < 1)
    pi_estimate = 4.0 * total_count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# 5. Dask-based Monte Carlo Pi estimation
def estimate_pi_dask(num_samples):
    start_time = time.time()
    x = da.random.random(num_samples)
    y = da.random.random(num_samples)
    count = da.sum(x**2 + y**2 < 1).compute()
    pi_estimate = 4.0 * count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# 6. Ray-based Monte Carlo Pi estimation
@ray.remote
def count_inside(num_samples):
    count = sum(1 for _ in range(num_samples) if random.random()**2 + random.random()**2 < 1)
    return count

def estimate_pi_ray(num_samples, batch_size=100000):
    start_time = time.time()
    ray.init(ignore_reinit_error=True)  # Initialize Ray inside function
    num_batches = num_samples // batch_size
    remainder = num_samples % batch_size
    # Launch batches in parallel
    batch_results = [count_inside.remote(batch_size) for _ in range(num_batches)]
    if remainder > 0:
        batch_results.append(count_inside.remote(remainder))
    
    total_count = sum(ray.get(batch_results))  # Aggregate results
    pi_estimate = 4.0 * total_count / num_samples
    ray.shutdown()  # Shutdown Ray to free memory
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# def estimate_pi_ray(num_samples):
#     start_time = time.time()
#     ray.init(ignore_reinit_error=True)  # Initialize Ray inside function
#     count = sum(ray.get([inside_ray.remote(i) for i in range(num_samples)]))
#     ray.shutdown()  # Shutdown Ray to free memory
#     elapsed_time = time.time() - start_time
#     return 4.0 * count / num_samples, elapsed_time

# 7. Numba JIT-based Monte Carlo Pi estimation (Python openMP)
@jit(nopython=True, parallel=True)
def inside_openmp(num_samples):
    count = 0
    for _ in prange(num_samples):  # prange enables parallelism
        x, y = np.random.random(), np.random.random()
        if x*x + y*y < 1:
            count += 1
    return count

def estimate_pi_openmp(num_samples):
    start_time = time.time()
    count = inside_openmp(num_samples)  # Parallel computation
    pi_estimate = 4.0 * count / num_samples
    elapsed_time = time.time() - start_time
    return pi_estimate, elapsed_time

# 8. OPEN-MPI Pi estimation in subprocess
# will be called with: 
# piexec --use-hwthread-cpus -n $(nproc) python mpi_pi_calc.py {num_samples}

# Benchmarking
## large
sample_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000, 1_000_000_000, 5_000_000_000, 10_000_000_000]
## small
# sample_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000]
chunk_size=100_000_000
spark_times, serial_times, mp_times, numpy_times, dask_times, ray_times, mpi_times = [], [], [], [], [], [], []
numba_times = []

for num_samples in sample_sizes:
    print(f"\nRunning benchmarks for {num_samples} samples...")
    
    print(f"Running Spark...")
    pi_spark, time_spark = estimate_pi_spark(num_samples)
    print(f"(Spark) Estimated Pi: {pi_spark:.8f} | Time: {time_spark:.4f}s")
    
    print(f"Running Serial Python...")
    pi_serial, time_serial = estimate_pi_serial(num_samples)
    print(f"(Serial) Estimated Pi: {pi_serial:.8f} | Time: {time_serial:.4f}s")
    
    print(f"Running Multiprocessing Python...")
    pi_mp, time_mp = estimate_pi_multiprocessing(num_samples,chunk_size)
    print(f"(Multiprocessing) Estimated Pi: {pi_mp:.8f} | Time: {time_mp:.4f}s")
    
    print(f"Running NumPy Vectorized Python...")
    pi_numpy, time_numpy = estimate_pi_numpy(num_samples,chunk_size)
    print(f"(NumPy) Estimated Pi: {pi_numpy:.8f} | Time: {time_numpy:.4f}s")
    
    print(f"Running Dask Parallel Computing...")
    pi_dask, time_dask = estimate_pi_dask(num_samples)
    print(f"(Dask) Estimated Pi: {pi_dask:.8f} | Time: {time_dask:.4f}s")
    
    print(f"Running Ray Parallel Computing...")
    pi_ray, time_ray = estimate_pi_ray(num_samples)
    print(f"(Ray) Estimated Pi: {pi_ray:.8f} | Time: {time_ray:.4f}s")

    print(f"Running Numba JIT Python...")
    pi_numba, time_numba = estimate_pi_openmp(num_samples)
    print(f"(Numba) Estimated Pi: {pi_numba:.8f} | Time: {time_numba:.4f}s")

    print(f"Running MPI Parallel Computing...")
    output_file = f"mpi_results.bin"
    # Execute MPI command
    command = f"mpiexec --use-hwthread-cpus -n $(nproc) python mpi_pi_calc.py {num_samples}"
    subprocess.run(command, shell=True, check=True)
    # Wait for the file to be created
    time.sleep(1)
    # Read from the output file
    if os.path.exists(output_file):
        with open(output_file, "rb") as f:
            data = f.read().decode().strip()
            pi_mpi, time_mpi = map(float, data.split(","))
        print(f"Loaded MPI Output - Pi: {pi_mpi}, Time: {time_mpi}s")
    else:
        print(f"Warning: Output file {output_file} not found!")

    spark_times.append(time_spark)
    serial_times.append(time_serial)
    mp_times.append(time_mp)
    numpy_times.append(time_numpy)
    dask_times.append(time_dask)
    ray_times.append(time_ray)
    numba_times.append(time_numba)
    mpi_times.append(time_mpi)

print()
print(f"Loading GPU calculations from COLab with Tesla T4...")
# Data from Colab runs
data = {
    "num_samples": [
        10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000,
        50_000_000, 100_000_000, 500_000_000, 1_000_000_000, 5_000_000_000, 10_000_000_000
    ],
    "CuPy_time": [
        0.0020, 0.0024, 0.0019, 0.0018, 0.0018, 0.0022, 0.0019, 0.0030, 0.0039, 
        0.0144, 0.1355, 7.7530, 17.5241
    ],
    "JAX_time": [
        0.0047, 0.0035, 0.0044, 0.0061, 0.0051, 0.0043, 0.0044, 0.0164, 0.0307, 
        0.1467, 0.2878, 1.4555, 3.0754
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Plot results
plt.figure(figsize=(8, 5))
plt.plot(sample_sizes, spark_times, marker='o', linestyle='-', label="Spark")
plt.plot(sample_sizes, serial_times, marker='s', linestyle='-', label="Serial Python")
plt.plot(sample_sizes, mp_times, marker='^', linestyle='-', label="Multiprocessing")
plt.plot(sample_sizes, numpy_times, marker='d', linestyle='-', label="NumPy Vectorized")
plt.plot(sample_sizes, dask_times, marker='x', linestyle='-', label="Dask Parallel")
plt.plot(sample_sizes, ray_times, marker='p', linestyle='-', label="Ray Parallel")
plt.plot(sample_sizes, numba_times, marker='*', linestyle='-', label="Numba JIT")
plt.plot(sample_sizes, mpi_times, marker='h', linestyle='-', label="MPI Parallel")
plt.plot(df["num_samples"], df["CuPy_time"], marker='v', linestyle='-', label="CuPy GPU")
plt.plot(df["num_samples"], df["JAX_time"], marker='>', linestyle='-', label="JAX GPU")
plt.xlabel("Number of Samples")
plt.ylabel("Execution Time (seconds)")
plt.xscale("log")
plt.grid(True)
plt.legend()
plt.show()
