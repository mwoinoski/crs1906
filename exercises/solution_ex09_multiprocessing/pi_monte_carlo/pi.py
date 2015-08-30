"""
pi.py - Example of Python multiprocessing.

Monte Carlo approximation of pi.

Original version appeared in "Python High Performance Programming", by
Gabriele Lanaro.

This version has modifications to use the concurrent.futures module.
"""

from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
)
import random

# Monte Carlo is not an efficient strategy. Even with 10**9 samples, the value
# of pi produced is accurate only to 5 digits. But we'll keep the number of
# samples small so it doesn't take too long to run.
total_samples = 10**6


def calculate_one_sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    return 1 if x**2 + y**2 <= 1 else 0


def pi_serial():
    """Perform the Monte Carlo technique in a serial fashion"""
    # call sample_one() a million times, add up all the values
    hits = sum(calculate_one_sample() for _ in range(total_samples))
    pi = 4.0 * hits/total_samples
    return pi


def sample_multiple(chunk_size):
    # call sample_one() a million/chunk_size times, then add up all the values
    return sum(calculate_one_sample() for _ in range(chunk_size))


def pi_async():
    """
    Divide the calculation into four chunks and create a process to execute
    each chunk.

    This calculation is an example of an Embarrassingly Parallel problem,
    which means that it's very easy to break the problem up into separate tasks.
    Tasks don't need to coordinate or share data in any way, so there's no
    need for inter-process communication, locking, etc. We like
    Embarrassingly Parallel problems :)
    """
    ntasks = 4
    # call multiprocessing.cpu_count() for number of (virtual) CPU cores
    
    chunk_size = total_samples//ntasks  # divide work into 4 chunks
    
    # with ThreadPoolExecutor(max_workers=ntasks) as executor:
    with ProcessPoolExecutor() as executor:
        # spawn 4 processes. Each one calls sample_multiple() chunk_size times
        futures = [executor.submit(sample_multiple, chunk_size)
                   for _ in range(ntasks)]

    # get the result of each process as it completes and add it to the total
    hits = sum(future.result() for future in as_completed(futures))
    # hits = sum(future.result() for future in futures)
    
    pi = 4.0 * hits/total_samples
    return pi


if __name__ == '__main__':
    print('pi_async() returned {}'.format(pi_async()))

    from timeit import timeit

    time = timeit('pi_async()',
                  setup='from __main__ import pi_async',
                  number=1)
    print('pi_async() finished in {:.3} seconds'.format(time))

    time = timeit('pi_serial()',
                  setup='from __main__ import pi_serial',
                  number=1)
    print('pi_serial() finished in {:.3} seconds'.format(time))
