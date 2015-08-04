"""
measure.py - defines a profiling decorator

Usage:
    from measure import measure, get_function_stats

    @measure
    def my_func(args):
        ...

    stats = get_function_stats()  # returns list of tuples
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import time
from functools import wraps

# Dictionary for accumulated function statistics.
# Each key is a function name.
# Each value is a two-item list of the total number of calls to the function
# and the total execution time of all calls.
_function_stats = {}


def measure(func):
    """
    Decorator that accumulates number of calls and average run time of each
    call for the decorated function.
    """
    # If the decorator function is not already in the accumulator
    # dictionary, add it. This assures that all decorated functions will be
    # in the dictionary, even if they're never called.
    func_name = func.__name__
    if func_name not in _function_stats:
        _function_stats[func_name] = [0, 0]

    @wraps(func)  # func is a reference to the decorated function
    def wrapper(*args, **kwargs):
        """wrapper() will be called when the decorated function is called"""
        start = time.process_time()  # get initial timestamp
        r = func(*args, **kwargs)    # call decorated function
        end = time.process_time()    # get ending timestamp
        run_time = end - start
        stats = _function_stats[func_name]  # get this function's stats
        stats[0] += 1                       # update stats
        stats[1] += run_time
        # wrapper returns the result of the call to the decorated function
        return r

    # measure function returns reference to wrapper function
    return wrapper


def get_function_stats():
    """
    Returns list of 3-tuple:
        (function-name, number-of-calls, average-time-per-call)
    """
    return [(name, calls, total_time/calls if calls > 0 else 0)
            for name, (calls, total_time) in sorted(_function_stats.items(),
                                                    key=lambda x: x[0])]
