"""
sample_mod2.py - Sample module from setup_example
"""

from .utils import util_mod2


def func2():
    print("In {}.func2()".format(__name__))
    util_mod2.util_func2()
