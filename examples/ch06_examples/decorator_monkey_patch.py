"""
decorator_monkey_patch.py - example of a decorator applied with a monkey patch
"""

import time


def measure(target_func):

    def wrapper(*args, **kwargs):
        start = time.time()
        result = target_func(*args, **kwargs)
        end = time.time()
        print(f'{target_func.__name__}: {end - start:.4f} secs')
        return result

    return wrapper


def read_protected_file(filepath, pass_phrase):
    time.sleep(.2)
    return 'Mischief Managed!'

print('\n==== Calling read_protected_file() before applying decorator ====')

data = read_protected_file('magic_spells.prot', 'Hogworts')
print('read_protected_file() returned', data)

read_protected_file = measure(read_protected_file)

print('\n==== Calling read_protected_file() after applying decorator ====')

data = read_protected_file('magic_spells.prot', 'Hogworts')
print('read_protected_file() returned', data)
