"""
profiling_decorator.py - defines a decorator for profiling function
execution time

Usage example:
    @profile_call
    def my_func(a, b, c):
        ...
"""

import time
from decorators import format_args


def profile_call(target_func):
    """decorator for profiling function execution time"""

    def wrapper(*args, **kwargs):
        """Nested function definition"""
        start = time.process_time()
        # Call target function
        result = target_func(*args, **kwargs)  # unwrap the argument list
        end = time.process_time()
        print('{}({}): {} secs'.format(
            target_func.__name__, format_args(*args, **kwargs),
            end - start))
        return result

    # Decorator function returns reference to nested wrapper function
    return wrapper
