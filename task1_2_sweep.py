import time
import csv
import statistics
from concurrent.futures import ThreadPoolExecutor
import threading

TRIALS = 7


def worker_task(thread_id, team_size):
    _ = threading.get_native_id()
    return thread_id


def run_team_timed(num_threads):
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task, tid, num_threads) for tid in range(num_threads)]
        for f in futures:
            f.result()
    t1 = time.perf_counter()
    return t1 - t0


if __name__ == "__main__":
    P_values = [1, 2, 4, 8, 16, 32, 64]
    rows = []
    for P in P_values:
        times = [run_team_timed(P) for _ in range(TRIALS)]
        mean_t = statistics.mean(times)
        stdev_t = statistics.stdev(times) if len(times) > 1 else 0.0
        rows.append((P, mean_t * 1000, stdev_t * 1000))
        print(f"P={P:3d} | mean={mean_t*1000:8.4f} ms | stdev={stdev_t*1000:7.4f} ms | trials={times}")

    with open("task1_2_oversubscription.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["P", "mean_time_ms", "stdev_time_ms"])
        for r in rows:
            w.writerow(r)
