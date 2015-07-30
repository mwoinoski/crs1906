__author__ = 'Mike Woinoski mike@articulatedesign.us.com'

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'nose',
    'pytest',
    'pytest-cov',
    'WebTest',      # Runs a WSGI application for integration tests
    'Sphinx',       # Generates documentation from docstrings in source code
]

setup(name='TicketManor',
      version='1.0.0',
      description='TicketManor',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Framework :: SQLAlchemy",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Mike Woinoski',
      author_email='michaelw@articulatedesign.us.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ticketmanor',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = ticketmanor:main
      [console_scripts]
      initialize_TicketManor_db = ticketmanor.scripts.initializedb:main
      """,
      )
