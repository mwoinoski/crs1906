"""
primes_python.py - Defines a function that calculates the first n prime numbers
"""

def primes_python(how_many):
    limit = 10000
    result = []
    if how_many <= 0 or how_many > limit:
        print("{} is too many, let's do {} instead..."
              .format(how_many, limit))
        how_many = limit
    k = 0
    n = 2
    while k < how_many:
        i = 0
        while i < k and n % result[i] != 0:
            i += 1
        if i == k:
            k += 1
            result.append(n)
        n += 1
    return result

if __name__ == '__main__':
    import time
    start_time = time.time()
    how_many = 10000
    print("calling primes_python({})...".format(how_many))
    primes = primes_python(how_many)
    last_5 = [primes[i] for i in range(how_many-5, how_many)]
    end_time = time.time()
    print("tail of primes list: {}".format(last_5))
    print("Total execution time: {:.1f} seconds".format(end_time-start_time))
