"""
integrate.pyx - Implementation of numerical integration: calculates
the numerical value of a definite integral using an iterated rule.

Implemented in Cython
"""

def f(double x):
    return x**2 - x


def integrate_f(double a, double b, int N):
    cdef int i
    cdef double s, dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
