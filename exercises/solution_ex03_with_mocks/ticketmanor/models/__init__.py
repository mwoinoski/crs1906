"""
package script for models package.

Defines classes and functions required for interacting with SQLAlchemy.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
# from zope.sqlalchemy import ZopeTransactionExtension  # SQLAlchemy 1.0

DBSession = scoped_session(sessionmaker())
# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))  # SQLAlchemy 1.0
Base = declarative_base()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
