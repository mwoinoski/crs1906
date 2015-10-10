"""
setup.py - Set up script for an application.
"""

from setuptools import setup
from Cython.Build import cythonize


setup(
    name='Cython Demo App',
    ext_modules=cythonize('*.pyx')
    )

# External C modules are declared in the modules that use them.
# For an example, see primes_c_wrapper.py
