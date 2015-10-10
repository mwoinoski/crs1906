"""
primes_cython.pyx - Defines a Cython function that calculates the
first n prime numbers
"""

def primes_cython(int how_many):
    DEF Limit = 10000  # DEF defines a compile-time constant
    cdef int n, k, i
    cdef int p[Limit]
    result = []
    if how_many <=0 or how_many > Limit:
        print("{} is too many, let's do {} instead..."
              .format(how_many, Limit))
        how_many = Limit
    k = 0
    n = 2
    while k < how_many:
        i = 0
        while i < k and n % p[i] != 0:
            i = i + 1
        if i == k:
            p[k] = n
            k = k + 1
            result.append(n)
        n = n + 1
    return result