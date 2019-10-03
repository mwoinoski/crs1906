"""
measure.py - defines a profiling decorator

Usage:
    from measure import measure, get_function_stats

    @measure
    def my_func(args):
        ...

    stats = get_function_stats()  # returns list of tuples
"""

import time
from functools import wraps

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

# TODO: note the initialization of the _function_stats dictionary, which will
# be used to accumulate statistics for all measured functions.
# Each key is a function name.
# Each value is a two-item list of the total number of calls to the function
# and the total execution time of all calls.
# (no code change required)
_function_stats = {}


# TODO: note the definition of the measure decorator. Make sure you understand
# how it works.
# (no code change required)
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

    @wraps(func)  # For details of @wraps decorator, see note at end of file.
    # `func` is a reference to the decorated function
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


# TODO: note the definition of the get_function_stats() function. This function
# returns statistics about all measured functions. Make sure you understand
# how it works.
# (no code change required)
def get_function_stats():
    """
    Returns a list of 3-tuples. Each tuple contains the name of a function,
    the number of calls to that function, and the average time per call:
        (function-name, number-of-calls, average-time-per-call)
    """
    return [(name, calls, total_time/calls if calls > 0 else 0)
            for name, (calls, total_time) in sorted(_function_stats.items())]

    # Implementation without list comprehension:
    # stats = []
    # sorted_items = sorted(_function_stats.items())
    # for name, (calls, total_time) in sorted_items:
    #     if calls > 0:
    #         time_per_call = total_time/calls
    #     else:
    #         time_per_call = 0
    #     stats.append((name, calls, time_per_call))
    # return stats
                                                    
'''
@wraps is a standard decorator that can be used on a custom decorator's
wrapper function. @wraps solves the problem that a function's __name__
and __doc__ attributes appear to be set incorrectly when that function is
decorated. For example, if the function check() is decorated with the
@measure decorator defined in this file:

    @measure
    def check(self, level=0):
        """Puzzle level 0"""
        ...

Without @wraps, the __name__ and __doc__ attributes get values from the
decorator's wrapper function:
    print('Name:', check.__name__)       # Name: wrapper
    print('Doc string:', check.__doc__)  # Doc string: wrapper() will be ...

With @wraps, the __name__ and __doc__ attributes get values from the
decorated function, not the wrapper function:
    print('Name:', check.__name__)       # Name: check
    print('Doc string:', check.__doc__)  # Doc string: Puzzle level 0
'''