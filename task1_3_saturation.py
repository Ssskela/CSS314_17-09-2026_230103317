import time
import math
import os
import csv
from concurrent.futures import ThreadPoolExecutor

WORK_PER_THREAD = 10_000_000


def cpu_bound_work(thread_id):
    # 10,000,000 floating point sqrt operations, as specified in the manual
    total = 0.0
    for i in range(WORK_PER_THREAD):
        total += math.sqrt(i + 1)
    return total


def run_saturation(num_threads):
    t0 = time.perf_counter()
    cpu0 = os.times()  # (user, system, children_user, children_system, elapsed)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(cpu_bound_work, tid) for tid in range(num_threads)]
        for f in futures:
            f.result()
    cpu1 = os.times()
    t1 = time.perf_counter()

    wall = t1 - t0
    user_cpu = cpu1.user - cpu0.user
    sys_cpu = cpu1.system - cpu0.system
    total_cpu = user_cpu + sys_cpu
    # "CPU utilization" proxy: total CPU-seconds consumed / wall-clock seconds
    # (would equal num_cores if perfectly parallel across that many cores)
    utilization_ratio = total_cpu / wall if wall > 0 else 0
    return wall, total_cpu, utilization_ratio


if __name__ == "__main__":
    print(f"Logical CPUs available in this environment: {os.cpu_count()}")
    P_values = [1, 2, 4]  # kept small: this is a CPU-bound Python loop under the GIL
    rows = []
    for P in P_values:
        wall, cpu_time, ratio = run_saturation(P)
        rows.append((P, wall, cpu_time, ratio))
        print(f"P={P} | Wall={wall:.3f}s | CPU-time={cpu_time:.3f}s | Utilization ratio (CPU-time/Wall)={ratio:.2f}")

    with open("task1_3_saturation.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["P", "wall_seconds", "cpu_seconds", "utilization_ratio"])
        for r in rows:
            w.writerow(r)
