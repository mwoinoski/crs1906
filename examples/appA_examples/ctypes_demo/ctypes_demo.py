"""
ctypes_demo.py - Demo of calling C functions using ctypes module
"""

from ctypes import cdll, c_int, cast, POINTER
import array
from os.path import abspath, join, split

# .dll file is located in the current directory.
# To build the DLL, run:  make

library = 'primes.dll'

library = join(*(split(abspath(__file__))[:-1] + (library,)))
print("Loading DLL from " + library)

library_mod = cdll.LoadLibrary(library)

# The type of ctypes.cdll is ctypes.LibraryLoader. If you reference an
# attribute with the same name as a DLL, the LibraryLoader loads the DLL.
# So the following can replace the call to LoadLibrary:
# library_mod = cdll.primes

# int is_prime(int)
is_prime = library_mod.is_prime  # assign function reference to a variable
is_prime.argtypes = (c_int,)
is_prime.restype = c_int

n = 28

c_result = is_prime(n)  # call C function using the function reference

print("{} is{} prime".format(n, "" if c_result == 1 else " not"))

n = 29
c_result = is_prime(n)  # call C function using the function reference
print("{} is{} prime".format(n, "" if c_result == 1 else " not"))

# int primes_c(int, int *)
primes_c = library_mod.primes_c
primes_c.argtypes = (c_int, POINTER(c_int))
primes_c.restype = c_int

# create a ctype array for the buffer argument to primes_c().
ctypes_array_class = c_int * 10000
print("type of ctypes_array_class is", type(ctypes_array_class))
ctypes_array = ctypes_array_class()
print("type of ctypes_array is", type(ctypes_array))

# We could combine the previous two statements into one:
# ctypes_array = (c_int * 10000)()

# Call the C function, passing a ctypes array as the second argument
c_result = primes_c(10000, ctypes_array)

# Retrieve values from the array just like an ordinary Python list
last_5 = [ctypes_array[i]
          for i in range(9995, 10000)]
print("c_result: {}, tail of ctypes_array: {}".format(c_result, last_5))

# Or copy the ctypes array elements to an ordinary Python list
primes_list = list(ctypes_array)
assert primes_list == list(ctypes_array)

print("len(ctypes_array): {}, len(primes_list): {}"
      .format(len(ctypes_array), len(primes_list)))

# Another strategy for passing an array to a C function: use the built-in
# array module to create an array of int, initialized to all zeros
primes_array = array.array('i', [0]*10000)

# The C function needs the address of the buffer
primes_ptr, _ = primes_array.buffer_info()

# Call the C function, passing the address of the buffer
c_result = primes_c(10000,
                    cast(primes_ptr, POINTER(c_int)))

# Retrieve values from the array as usual
last_5 = [primes_array[i]
          for i in range(9995, 10000)]
print("c_result: {}, tail of primes_array: {}".format(c_result, last_5))
