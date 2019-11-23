__author__ = 'Mike Woinoski mike@articulatedesign.us.com'

import os

from setuptools import setup, find_packages, Command
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

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'coverage',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy < 1.2',
    'waitress',
    'pytest-cov',
    'pytest',
    'mysql-connector-python',
    'WebTest',      # Runs a WSGI application for integration tests
    'Sphinx',       # Generates documentation from docstrings in source code
]

setup(name='Exercise_2_1',
      version='1.0.0',
      description='Exercise 2.1',
      long_description=README + '\n\n' + CHANGES,
      author='Mike Woinoski',
      author_email='mike@articulatedesign.us.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ticketmanor',
      install_requires=requires,
      cmdclass={'clean': CleanCommand},  # use CleanCommand class defined above
      entry_points="""\
      [paste.app_factory]
      main = ticketmanor:main
      [console_scripts]
      initialize_TicketManor_db = ticketmanor.scripts.initializedb:main
      """
      )
