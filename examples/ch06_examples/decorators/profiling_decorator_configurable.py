"""
profiling_decorator.py - defines a decorator for profiling function execution time

Usage example:
    @profile_call
    def my_func(a, b, c):
        ...
"""

from functools import wraps
from time import process_time
from configparser import ConfigParser
from decorators import format_args

config = ConfigParser()
config.read('config/config.ini')
profiling_enabled = config['ticketmanor.com'].getboolean('profiling.enabled')


def decorator_disabled(decorated_fn):
    return decorated_fn


def profile_call_enabled(decorated_fn):
    @wraps(decorated_fn)
    def profile(*args, **kwargs):
        before = process_time()

        # call the decorated function
        result = decorated_fn(*args, **kwargs)  # unwrap the argument list

        print(f'{decorated_fn.__name__}({format_args(*args, **kwargs)})',
              f'ran in {process_time() - before} secs')
        return result

    # outer function returns reference to nested function
    return profile


# if configured, apply decorator with monkey patch
profile_call = profile_call_enabled if profiling_enabled \
                                    else decorator_disabled
