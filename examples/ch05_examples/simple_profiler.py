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

        print(f'{func.__module__}.{func.__name__}() : {end - start:.4f} seconds')
        return r
        # To add the function's arguments to the output, you can do something
        # like this:
        # all_args = [str(a) for a in args]
        # all_args.extend([str(k)+'='+str(v) for k, v in kwargs.items()])
        # args_str = ', '.join(all_args)
        # print(f'{func.__module__}.{func.__name__}({args_str}) : {end - start:.4f} seconds')

    return wrapper
