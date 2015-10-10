"""
primes_ex_mod_demo.py - Uses an extension module written in C
"""

import array

# Import extension module
from primes_ext_mod import is_prime, primes_c

n = 28
# call function from extension module
print("{} is{} prime".format(n, "" if is_prime(n) else " not"))

n = 29
# call function from extension module
print("{} is{} prime".format(n, "" if is_prime(n) else " not"))

how_many = 10000
primes_buffer = array.array('i', [0] * how_many)

# Call function from extension module, passing the Python array object
result = primes_c(how_many, primes_buffer)

# Retrieve values from the array as usual
last_5 = [primes_buffer[i] for i in range(how_many-5, how_many)]
print("tail of primes_array: {}".format(last_5))

