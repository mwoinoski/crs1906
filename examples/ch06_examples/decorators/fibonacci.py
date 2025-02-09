"""
fibonacci.py - Calculate the Fibonacci series (caches results)
"""

known = {0: 0, 1: 1}  # cache of known results


def fibonacci(n):
    assert(n >= 0), 'n must be >= 0'
    if n in known:
        return known[n]
    res = fibonacci(n-1) + fibonacci(n-2)
    known[n] = res
    return res


if __name__ == '__main__':
    from timeit import Timer
    t = Timer('fibonacci(100)', 'from __main__ import fibonacci')
    print(f"Time: {t.timeit():.2} usecs")
