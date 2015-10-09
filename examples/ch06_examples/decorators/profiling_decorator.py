"""
profiling_decorator.py - defines a decorator for profiling function
execution time

Usage example:
    @profile_call
    def my_func(a, b, c):
        ...
"""

from time import process_time
from decorators import format_args


def profile_call(decorated_fn):
    """decorator for profiling function execution time"""
    def profile(*args, **kwargs):
        before = process_time()

        # call the decorated function
        result = decorated_fn(*args, **kwargs)  # unwrap the argument list

        print('{}({}) ran in {} secs'.format(
            decorated_fn.__name__, format_args(*args, **kwargs),
            process_time() - before))
        return result

    # outer function returns reference to nested function
    return profile
