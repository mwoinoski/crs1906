# distutils: language = c
# distutils: sources = primes_c.c
"""
primes_c_wrapper.pyx - Wraps a call to a C function that calculates
the first n prime numbers.

The "distutils" comments above are directives to Cython. They must be the
very first lines in the file (don't precede them with a docstring, etc.)

For details about referencing C++ objects and calling C++ methods, see
http://docs.cython.org/src/userguide/wrapping_CPlusPlus.html
"""

from libc.stdlib cimport calloc, free

cdef extern from "primes_c.h":
    int primes_c(int how_many, int p[])


def primes_c_wrapper(int how_many):
    """Wrap a C function"""

    limit = 10000
    if how_many <= 0 or how_many > limit:
        print("{} is too many, let's do {} instead..."
              .format(how_many, limit))
        how_many = limit

    # Use a Cython C-API function to allocate a buffer for the array of primes.
    # This memory is accounted for in Python's internal memory management system.

    cdef int *buffer = <int *>calloc(how_many, sizeof(int))

    if not buffer:
        raise MemoryError()

    try:
        # Pass the allocated memory to the C function
        result = primes_c(how_many, buffer)

        # Copy the items from the allocated memory to a Python list
        return [buffer[i] for i in range(result)]
    finally:
        free(buffer)  # Return memory to the system

