r"""
cache_decorator_demo.py: a client of the cache decorator.
"""

from timeit import Timer
from cache_decorator import cache
from logging_decorator import log_call


@cache
def nsum(n):
    """Return the sum of the first n numbers using a recursive function"""
    assert(n >= 0), "n must be >= 0"
    return 0 if n == 0 else n + nsum(n-1)


@cache
def fibonacci(n):
    """Returns the nth number of the Fibonacci sequence using a recursive function"""
    assert(n >= 0), "n must be >= 0"
    return n if n in (0, 1) else fibonacci(n-1) + fibonacci(n-2)


if __name__ == "__main__":
    # Because the cache decorator caches the results of previous function calls,
    # expensive calls can be skipped.
    # TODO: run this program once as-is, then comment out the @cache statements
    #       on the functions above and run the program again. You'll see a
    #       dramatic difference in execution time.

    t = Timer("fibonacci(5)", "from __main__ import fibonacci")
    print(f"executing: fibonacci(5), average time: {t.timeit(number=2_000_000):.2f} usecs")

    t = Timer("nsum(5)", "from __main__ import nsum")
    print(f"executing: nsum(5), average time: {t.timeit(number=2_000_000):.2f} usecs")
