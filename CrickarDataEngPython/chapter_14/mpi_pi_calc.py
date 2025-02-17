import time
import random
import sys
from mpi4py import MPI



# Get number of samples from command line argument
num_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 100000

start_time = time.time()

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Divide workload
local_samples = num_samples // size
local_count = sum(1 for _ in range(local_samples) if random.random()**2 + random.random()**2 < 1)

# Reduce results to rank 0
total_count = comm.reduce(local_count, op=MPI.SUM, root=0)

# Only rank 0 writes to file
if rank == 0:
    pi_estimate = 4.0 * total_count / num_samples
    elapsed_time = time.time() - start_time

    # Use a unique filename for each run
    output_file = f"mpi_results.bin"

    # Write results to a binary file
    with open(output_file, "wb") as f:
        f.write(f"{pi_estimate},{elapsed_time}\n".encode())

    print(f"(MPI) Estimated Pi: {pi_estimate:.8f} | Time: {elapsed_time:.4f}s | Saved to {output_file}")
