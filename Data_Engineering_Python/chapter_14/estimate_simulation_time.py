import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Given sample sizes and execution times
sample_sizes = np.array([10_000, 50_000, 100_000, 500_000, 1_000_000, 
                         5_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000])

spark_times = np.array([5.82, 1.16, 1.20, 1.23, 1.30, 2.05, 2.93, 10.22, 19.04, 89.77])
serial_times = np.array([0.0043, 0.0363, 0.0452, 0.1638, 0.2848, 1.3371, 2.6355, 12.8572, 25.6138, 128.74])
multiprocessing_times = np.array([0.0259, 0.0292, 0.0400, 0.1102, 0.2014, 0.9628, 1.9304, 10.2207, 20.4923, 75.19])
numpy_times = np.array([0.0009, 0.0021, 0.0042, 0.0205, 0.0334, 0.1344, 0.267, 1.2488, 2.9795, 17.75])

# Additional large sample sizes to **extrapolate**
additional_samples = np.array([1_000_000_000, 5_000_000_000, 10_000_000_000])

# **Polynomial regression for extrapolation**
def extrapolate(x, y, x_new):
    coeffs = np.polyfit(np.log(x), np.log(y), deg=3)  # Quadratic fit in log-log scale
    log_y_new = np.polyval(coeffs, np.log(x_new))
    return np.exp(log_y_new)

# Apply **real extrapolation**
spark_extra = extrapolate(sample_sizes, spark_times, additional_samples)
serial_extra = extrapolate(sample_sizes, serial_times, additional_samples)
multiprocessing_extra = extrapolate(sample_sizes, multiprocessing_times, additional_samples)
numpy_extra = extrapolate(sample_sizes, numpy_times, additional_samples)

# Append the **extrapolated** values
sample_sizes = np.append(sample_sizes, additional_samples)
spark_times = np.append(spark_times, spark_extra)
serial_times = np.append(serial_times, serial_extra)
multiprocessing_times = np.append(multiprocessing_times, multiprocessing_extra)
numpy_times = np.append(numpy_times, numpy_extra)

# Create a Pandas DataFrame
df = pd.DataFrame({
    "Samples": sample_sizes,
    "Spark (s)": spark_times,
    "Serial Python (s)": serial_times,
    "Multiprocessing (s)": multiprocessing_times,
    "NumPy Vectorized (s)": numpy_times
})

# Compute **total estimated simulation time**
total_spark_time = np.nansum(spark_times)
total_serial_time = np.nansum(serial_times)
total_multiprocessing_time = np.nansum(multiprocessing_times)
total_numpy_time = np.nansum(numpy_times)

total_simulation_time = total_spark_time + total_serial_time + total_multiprocessing_time + total_numpy_time

# Convert **total time to Hours, Minutes, and Seconds**
hours = int(total_simulation_time // 3600)
minutes = int((total_simulation_time % 3600) // 60)
seconds = total_simulation_time % 60

# Display results
print(df)
print(f"\nTOTAL SIMULATION TIME ESTIMATE: {total_simulation_time:.2f} seconds")
print(f"Equivalent to: {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")

# Plot execution time vs. number of samples
plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, spark_times, marker='o', linestyle='-', label="Spark")
plt.plot(sample_sizes, serial_times, marker='s', linestyle='-', label="Serial Python")
plt.plot(sample_sizes, multiprocessing_times, marker='^', linestyle='-', label="Multiprocessing")
plt.plot(sample_sizes, numpy_times, marker='d', linestyle='-', label="NumPy Vectorized")

plt.xlabel("Number of Samples")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs. Number of Samples (Monte Carlo Pi Estimation)")
plt.xscale("log")  # Log scale for better visualization
plt.grid(True)
plt.legend()
plt.show()
