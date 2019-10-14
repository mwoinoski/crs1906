from ctypes import cdll, c_int
from sys import argv

library = 'primes.dll'
library_mod = cdll.LoadLibrary(library)

is_prime = library_mod.is_prime
is_prime.argtypes = (c_int,)
is_prime.restype = c_int

num = 29
# num = int(argv[1])  # get argument from command line
result = is_prime(num)

print(f'{num} is {"not " if result == 0 else ""}prime')
