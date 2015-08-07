"""
setup.py - Set up script for sample project
"""
from setuptools import setup, find_packages, Command
import codecs  # To use a consistent encoding
import os
from glob import glob
import shutil


class CleanCommand(Command):
    """Command class that will be used by 'setup.py clean'"""
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: ' + self.cwd
        for pattern in ['build', 'dist', '*.egg-info', '*.pyc', '*.tgz']:
            for name in glob(pattern):
                if os.path.isdir(name):
                    shutil.rmtree(name)
                else:
                    os.remove(name)

# Get the long description from the README.rst file.
# This will be become the contents of the project's home page on PyPI.
# Note that we can't assume that the Python interpreter's working directory is
# this directory, so we can't use a relative path to access README.rst
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='simple_tz',
    version='1.0.0',
    description='Wrapper for pytz functions',
    long_description=long_description,
    platforms=['all'],
    install_requires=['pytz'],
    author='Mike Woinoski',
    author_email='mike@wxyz.me',
    url='http://www.pythonchamp.com/simple_tz',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    cmdclass={'clean': CleanCommand},  # use CleanCommand class defined above
    license='MIT',
    keywords='simple_tz timezone datetime',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
