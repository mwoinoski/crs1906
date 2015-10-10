"""
measure.py - Profiling utilities
"""

from functools import wraps

try:
    from time import perf_counter
    timer_func = perf_counter
except ImportError:
    import time
    timer_func = time.time


def measure(func):
    """Decorator that times the execution of function"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = timer_func()  # get starting timestamp

        r = func(*args, **kwargs)  # call target function

        end = timer_func()   # get ending timestamp

        print('{}.{} : {:.4f} seconds'
              .format(func.__module__, func.__name__, end - start))
        return r
    return wrapper
