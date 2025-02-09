"""
integrate_python.py - Implementation of numerical integration: calculates
the numerical value of a definite integral using an iterated rule
"""

def f(x):
    return x**2 - x


def integrate_f(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
