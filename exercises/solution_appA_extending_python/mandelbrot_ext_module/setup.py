"""
setup.py - build file for C extension module.
"""

from setuptools import setup, Extension

# TODO: Complete the call to the setup() function.
# HINT: Module name is 'calc_z_ser_ext_mod'
#       Source files are named 'calc_z_ser.c' and 'calc_z_ser_ext_mod.c'
# HINT: see slide 7-17
setup(name='calc_z_ser_ext_mod',
      ext_modules=[
          Extension('calc_z_ser_ext_mod',
                    ['calc_z_ser.c', 'calc_z_ser_ext_mod.c'],
                    include_dirs=['.']
                    )])
