"""
profiling_decorator.py - defines a decorator for profiling function execution time

Usage example:
    @profile_call
    def my_func(a, b, c):
        ...
"""

import functools
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini")
profiling_enabled = config["ticketmanor.com"].getboolean("profiling.enabled")

def decorator_disabled(decorated_fn):
    return decorated_fn

def profile_call_enabled(decorated_fn):
    @functools.wraps(decorated_fn)
    def profile(*args):
        before = datetime.now()

        # call the decorated function
        result = decorated_fn(*args)  # unwrap the argument list

        after = datetime.now()
        delta = after - before
        print("{}({}) ran in {} usecs".format(
            decorated_fn.__name__, ",".join(str(a) for a in args), delta.microseconds))
        return result

    # outer function returns reference to nested function
    return profile

#
profile_call = profile_call_enabled if profiling_enabled \
                                    else decorator_disabled
