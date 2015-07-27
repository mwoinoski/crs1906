"""
setup.py
Builds the primes extension module:
    python setup.py build_ext --inplace
"""

from distutils.core import setup, Extension

setup(name="primes_ext_mod",
      ext_modules=[
        Extension("primes_ext_mod",    # extension module name
                  ["primes.c", "primes_ext_mod.c"],  # source files
                  include_dirs=['.'],  # directories with header files
                  )
        ]
)

# setup() will use the default compiler to compile and link the C files
# into an extension module.
# Default compiler is set in PYTHON_HOME\Lib\distutils\distutils.cfg

