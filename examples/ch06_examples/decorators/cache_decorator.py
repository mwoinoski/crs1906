"""
cache_decorator.py - defines a decorator for caching function results
"""

import functools


def cache(fn):
    cached_results = {}

    @functools.wraps(fn)
    def save_results(*args):
        if args not in cached_results:
            cached_results[args] = fn(*args)  # unwrap the argument list
        return cached_results[args]

    return save_results  # returns reference to function itself
