"""
logging_decorator.py - defines a decorator for logging function arguments and
results

Usage example:
    @log_call
    def my_func(a, b, c):
        ...
"""

from decorators import format_args  # defined in __init__.py


def log_call(fn):
    """Decorator for logging function arguments and results"""
    def log_args_and_results(*args, **kwargs):
        print(f'{fn.__name__}({format_args(*args, **kwargs)}): enter')

        # call the decorated function
        result = fn(*args, **kwargs)  # unwrap the argument lists

        print(f'{fn.__name__}({format_args(*args, **kwargs)}): exit,',
              f'result: {result}')
        return result

    # outer function returns reference to nested function
    return log_args_and_results
