"""
Customer model class
"""

__author__ = 'Mike Woinoski mike@articulatedesign.us.com'

from sqlalchemy import Column, Integer, ForeignKey
from .person import Person

class Customer(Person):
    """Model class for Customer
    """
    __tablename__ = 'customers'
    id = Column('id', Integer, ForeignKey('people.id'), primary_key=True)
