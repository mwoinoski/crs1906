"""
logging_decorator.py - defines a decorator for logging function arguments and results


Usage example:
    @log_call
    def my_func(a, b, c):
        ...
"""

import functools

def log_call(fn):
    @functools.wraps(fn)
    def log_args_and_results(*args):
        print("{}({}): enter".format(
            fn.__name__, ",".join(str(a) for a in args)))

        # call the decorated function
        result = fn(*args)  # unwrap the argument list

        print("{}({}): exit, result: {}".format(
            fn.__name__, ",".join(str(a) for a in args), result))
        return result

    # outer function returns reference to nested function itself
    return log_args_and_results
