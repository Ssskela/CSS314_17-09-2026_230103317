import time
import numpy as np
from numba import njit, prange


@njit(parallel=True)
def heat_step(u, u_next, alpha=0.20):
    rows, cols = u.shape

    for i in prange(1, rows - 1):
        for j in range(1, cols - 1):
            u_next[i, j] = u[i, j] + alpha * (
                u[i + 1, j]
                + u[i - 1, j]
                + u[i, j + 1]
                + u[i, j - 1]
                - 4.0 * u[i, j]
            )


GRID_SIZE = 1500
STEPS = 300

u = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32)
u_next = np.zeros_like(u)


# Dirichlet Boundary Conditions:
# Top and Left walls are maintained at 100 degrees Celsius
u[0, :] = 100.0
u[:, 0] = 100.0
u_next[0, :] = 100.0
u_next[:, 0] = 100.0


# Warmup JIT compilation
heat_step(u, u_next)


# Benchmark Execution
start = time.perf_counter()

for step in range(STEPS):
    heat_step(u, u_next)

    # Pointer swap avoids creating new arrays
    u, u_next = u_next, u


elapsed = time.perf_counter() - start

cells_per_sec = (
    (GRID_SIZE * GRID_SIZE * STEPS) / elapsed / 1e6
)


print(f"Heat Diffusion Complete: {elapsed:.3f} s")
print(f"Throughput: {cells_per_sec:.2f} Megacells/sec")



#(.venv) PS C:\Users\Asus\OpenMP_Python_Lab> & c:\Users\Asus\OpenMP_Python_Lab\.venv\Scripts\python.exe c:/Users/Asus/OpenMP_Python_Lab/challenge3.py
#Heat Diffusion Complete: 0.227 s
#Throughput: 2976.85 Megacells/sec

#(.venv) PS C:\Users\Asus\OpenMP_Python_Lab> & c:\Users\Asus\OpenMP_Python_Lab\.venv\Scripts\python.exe c:/Users/Asus/OpenMP_Python_Lab/challenge3.py
#Heat Diffusion Complete: 0.501 s
#Throughput: 1346.12 Megacells/sec

# A. Benchmark Results
# float64:
# Runtime = 0.227 s
# Throughput = 2976.85 Megacells/sec
#
# float32:
# Runtime = 0.501 s
# Throughput = 1346.12 Megacells/sec
#
# B. Float32 Comparison
# The runtime did not decrease in my experiment. Instead, the
# float32 version took 0.501 s compared with 0.227 s for float64.
# This means float32 was about 2.21x slower in this benchmark.
# Although float32 uses half the memory of float64, lower memory
# usage does not always guarantee better performance. The actual
# result can depend on CPU architecture, memory access patterns,
# Numba parallelization, and system load.
#
# C. Memory Roofline Model
# Adding twice as many CPU cores does not necessarily produce a
# 2x speedup because stencil computations are mainly limited by
# memory bandwidth. Once the memory bus is saturated, additional
# CPU cores have to wait for data from memory. Therefore, adding
# more cores gives little additional performance.