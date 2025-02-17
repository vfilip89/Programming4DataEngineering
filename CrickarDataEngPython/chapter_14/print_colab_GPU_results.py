import pandas as pd
import matplotlib.pyplot as plt

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
plt.plot(df["num_samples"], df["CuPy_time"], marker='o', linestyle='-', label="CuPy GPU")
plt.plot(df["num_samples"], df["JAX_time"], marker='s', linestyle='-', label="JAX GPU")
plt.xlabel("Number of Samples")
plt.ylabel("Execution Time (seconds)")
plt.xscale("log")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.title("GPU Performance Comparison: CuPy vs JAX")
plt.show()
