"""
setup.py - build file for C extension module.
"""

from setuptools import setup, Extension

# TODO: Complete the call to the setup() function.
setup(name='calc_z_ser_ext_mod',
      ext_modules=[
          Extension('calc_z_ser_ext_mod',
                    ['calc_z_ser.c', 'calc_z_ser_ext_mod.c'],
                    include_dirs=['.']
                    )])
