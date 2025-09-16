import subprocess
import time
import os

# Define sample sizes
sample_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]

mpi_results = []  # Store results

# Run MPI for each sample size
for num_samples in sample_sizes:
    output_file = f"mpi_results.bin"

    print(f"\nRunning MPI benchmark for {num_samples} samples...")
    
    # Execute MPI command
    command = f"mpiexec --use-hwthread-cpus -n $(nproc) python mpi_pi_calc.py {num_samples}"
    subprocess.run(command, shell=True, check=True)

    # Wait for the file to be created
    time.sleep(1)

    # Read from the output file
    if os.path.exists(output_file):
        with open(output_file, "rb") as f:
            data = f.read().decode().strip()
            pi_estimate, elapsed_time = map(float, data.split(","))

        mpi_results.append((num_samples, pi_estimate, elapsed_time))
        print(f"Loaded MPI Output - Pi: {pi_estimate}, Time: {elapsed_time}s")
    else:
        print(f"Warning: Output file {output_file} not found!")

# Print final results
print("\nFinal MPI Results:")
print(f"{'Samples':<15}{'Pi Estimate':<20}{'Time (s)':<10}")
for num_samples, pi_estimate, execution_time in mpi_results:
    print(f"{num_samples:<15}{pi_estimate:<20}{execution_time:<10}")
