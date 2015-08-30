"""
setup.py - build file for C extension module.
"""

from setuptools import setup, Extension

# TODO: complete the call to the setup() function.
# HINT: module name is 'calc_z_ser_ext_mod'
#       there is a single source file named 'calc_z_ser.c'
# HINT: see slide 7-17
setup(name='calc_z_ser_ext_mod',
      ext_modules=[
          Extension('calc_z_ser_ext_mod',
                    ['calc_z_ser.c', 'calc_z_ser_ext_mod.c'],
                    include_dirs=['.']
                    )])
