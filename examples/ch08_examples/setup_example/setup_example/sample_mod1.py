"""
sample_mod1.py - Sample module from setup_example
"""

from .utils import util_mod1


def func1():
    print("In {}.func1()".format(__name__))
    util_mod1.util_func1()
