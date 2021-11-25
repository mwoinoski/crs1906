"""
logging_method.py - Example of a decorator that logs function call parameters and return values
"""

def dumpArgs(func):
    """Decorator to print function call details - parameters names and effective values"""
    def wrapper(*func_args, **kwargs):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        arg_values = func_args[:len(arg_names)]
        defaults = func.__defaults__ or ()
        arg_values += defaults[len(defaults) - (func.__code__.co_argcount - len(arg_values)):]
        params = list(zip(arg_names, arg_values))
        arg_values = func_args[len(arg_names):]
        if arg_values: 
            params.append(('args', arg_values))
        if kwargs: 
            params.append(('kwargs', kwargs))
        params_list = ', '.join('{} = {!r}'.format(*item) for item in params)
        print(f"{func.__name__}({params_list})")
        return func(*func_args, **kwargs)
    return wrapper

@dumpArgs
def test(a, b = 4, c = 'blah-blah', *args, **kwargs):
    pass

test(11, 5, c='c value')
