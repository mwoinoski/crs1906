"""
pi.py - Monte Carlo approximation of pi.

Original version appeared in "Python High Performance Programming", by
Gabriele Lanaro.

This version has modifications to use Numba JIT compiler.
"""

from numba import jit
import random

# Monte Carlo is not an efficient strategy. Even with 10**9 samples, the value
# of pi produced is accurate only to 5 digits. But we'll keep the number of
# samples small so it doesn't take too long to run.
total_samples = 10**6


def calculate_one_sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    return 1 if x**2 + y**2 <= 1 else 0

@jit
def pi_serial():
    """Perform the Monte Carlo technique in a serial fashion"""
    # call sample_one() a million times, add up all the values
    hits = sum(calculate_one_sample() for _ in range(total_samples))
    pi = 4.0 * hits/total_samples
    return pi


if __name__ == '__main__':
    print(f'pi_serial() returned {pi_serial()}')

    from timeit import timeit

    time = timeit('pi_serial()',
                  setup='from __main__ import pi_serial',
                  number=1)
    print(f'pi_serial() finished in {time:.3} seconds')
