"""
fibonacci.py - Calculate the Fibonacci series (naive version)
"""


def fibonacci(n):
    assert(n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fibonacci(n-1) + fibonacci(n-2)


if __name__ == '__main__':
    from timeit import Timer
    t = Timer('fibonacci(5)', 'from __main__ import fibonacci')
    print(f"Time: {t.timeit():.2} usecs")
