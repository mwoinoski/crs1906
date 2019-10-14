"""
setup.py - build file for Cython extension module.
"""

from setuptools import setup
from Cython.Build import cythonize

# TODO: complete the call to the setup() function.
setup(name='Cython Mandelbrot extension module',
      ext_modules=cythonize('*.pyx',
                            compiler_directives={'language_level': '3'}))
