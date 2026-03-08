"""
Count the number primes less than a certain limit.
A CPU-bound algorithm implemented with threads.
"""

import time
import platform
import sysconfig

from math import sqrt
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

print("Python", platform.python_version())
is_free_threading_build = sysconfig.get_config_vars().get("Py_GIL_DISABLED") == 1
print(f"Free-threading build supported: {is_free_threading_build}")


# ---------------------------------------
# CPU‑bound workload
# ---------------------------------------
def count_primes(n: int) -> int:
    """Return the number of primes <= n using trial division."""
    count = 0
    for x in range(2, n + 1):
        is_prime = True
        r = int(sqrt(x))
        for d in range(2, r + 1):
            if x % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


# ---------------------------------------
# Worker that logs its own timing
# ---------------------------------------
def timed_worker(n: int, worker_id: int):
    start = time.perf_counter()
    result = count_primes(n)
    end = time.perf_counter()
    return {
        "worker": worker_id,
        "result": result,
        "start": start,
        "end": end,
        "elapsed": end - start,
    }


# ---------------------------------------
# Threaded benchmark using futures
# ---------------------------------------
def run_benchmark(n=100_000, num_threads=4):
    print(f"Running with n={n}, threads={num_threads}")

    overall_start = time.perf_counter()

    results = []
    # TODO: note the ThreadPoolExecutor that creates the worker threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(timed_worker, n, i)
            for i in range(num_threads)
        ]

        for fut in as_completed(futures):
            results.append(fut.result())

    overall_elapsed = time.perf_counter() - overall_start

    # Sort results by worker ID for readability
    results.sort(key=lambda r: r["worker"])

    print(f"\nTotal elapsed (wall‑clock) time: {overall_elapsed:.3f} seconds\n")

    print("Per‑thread timings:")
    for r in results:
        print(
            f"  Worker {r['worker']}: "
            f"{r['elapsed']:.3f}s (primes={r['result']})"
        )


if __name__ == "__main__":
    run_benchmark()
