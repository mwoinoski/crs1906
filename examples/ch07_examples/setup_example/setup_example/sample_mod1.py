"""
sample_mod1.py - Sample module from setup_example
"""

from .utils import util_mod1


def func1():
    print(f"In {__name__}.func1()")
    util_mod1.util_func1()
