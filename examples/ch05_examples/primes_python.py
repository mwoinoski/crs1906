"""
primes_python.py - Defines a function that calculates the first n prime numbers
"""

def primes_python(how_many):
    limit = 10000
    result = []
    if how_many <= 0 or how_many > limit:
        print(f"{how_many} is too many, let's do {limit} instead...")
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
    print(f"calling primes_python({how_many})...")
    primes = primes_python(how_many)
    last_5 = [primes[i] for i in range(how_many-5, how_many)]
    end_time = time.time()
    print(f"tail of primes list: {last_5}")
    print(f"Total execution time: {end_time - start_time:.1f} seconds")
