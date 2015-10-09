"""
decorator_demo.py - example of a decorator applied with '@'
"""

import time


def measure(target_func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = target_func(*args, **kwargs)
        end = time.time()
        print('{}: {:.4f} secs'.format(target_func.__name__, end - start))
        return result

    return wrapper


@measure
def read_protected_file(filepath, pass_phrase):
    time.sleep(.2)
    return 'Mischief Managed!'

print('\n==== Calling decorated read_protected_file() ====')

data = read_protected_file('magic_spells.prot', 'Hogworts')

print('read_protected_file() returned', data)
