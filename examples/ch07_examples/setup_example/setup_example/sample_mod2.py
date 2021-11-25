"""
sample_mod2.py - Sample module from setup_example
"""

from .utils import util_mod2


def func2():
    print(f"In {__name__}.func2()")
    util_mod2.util_func2()
