"""
test_primes.py - 
"""

from simple_profiler import measure

import primes_python
import primes_cython
import primes_c_wrapper


@measure
def calculate_cython(num):
    return primes_cython.primes_cython(num)


@measure
def calculate_python(num):
    return primes_python.primes_python(num)


@measure
def calculate_c_wrapper(num):
    return primes_c_wrapper.primes_c_wrapper(num)


def test_calc_primes():
    print()
    first_5000_python = calculate_python(5000)
    first_5000_cython = calculate_cython(5000)
    first_5000_pure_c = calculate_c_wrapper(5000)

    assert first_5000_cython == first_5000_python
    assert first_5000_python == first_5000_pure_c


if __name__ == '__main__':
    test_calc_primes()
