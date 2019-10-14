"""
primes_ext_mod_demo.py - Uses an extension module written in C
"""

import array

# Import extension module
from primes_ext_mod import is_prime, primes_c

n = 28
# call function from extension module
result = is_prime(n)
print(f'{n} is {"not " if result == 0 else ""}prime')

n = 1023
# call function from extension module
result = is_prime(n)
print(f'{n} is {"not " if result == 0 else ""}prime')

how_many = 10000
primes_buffer = array.array('i', [0] * how_many)

# Call function from extension module, passing the Python array object
result = primes_c(how_many, primes_buffer)

# Retrieve values from the array as usual
last_5 = [primes_buffer[i]
          for i in range(how_many-5, how_many)]
print(f'tail of primes_array: {last_5}')
