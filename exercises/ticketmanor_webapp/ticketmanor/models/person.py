"""
Person model class
"""

__author__ = 'Mike Woinoski mike@articulatedesign.us.com'

import json

from sqlalchemy import (
    Column,
    String,
    Integer,
)
# from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import composite

from . import Base
from .address import Address


class Person(Base):
    """
    Model class for Person
    """
    __tablename__ = 'people'
    id = Column('id', Integer, primary_key=True)  # autoincrement=True by default
    first_name = Column('firstname', String)
    middles = Column('middles', String)
    last_name = Column('lastname', String)
    email = Column('email', String)
    street = Column('street', String)
    city = Column('city', String)
    state = Column('state', String)
    country = Column('country', String)
    post_code = Column('postcode', String)
    # Address reference is to a composite/embedded instance
    address = composite(Address, street, city, state, country, post_code)
    # user_profile = relationship("UserProfile", uselist=False, backref="person")

    # Don't define __init__(): it breaks SQLAlchemy's magic

    @hybrid_property
    def name(self):
        # Client code accesses the hybrid property as an attribute: person.name
        middle_name = self.middles + " " if self.middles is not None else ""
        return "{self.first_name} {}{self.last_name}"\
            .format(middle_name, self=self)

    def __eq__(self, other):
        """Compare Person instances."""
        # Because the Person's Address is declared as a composite,
        # you must compare the address attributes of the Persons.
        # Don't delegate the address comparison to
        # Address.__eq__(), because SQLAlchemy may create a
        # dictionary to hold the values rather than an Address.
        return isinstance(other, Person) and \
            other.id == self.id and \
            other.first_name == self.first_name and \
            other.middles == self.middles and \
            other.last_name == self.last_name and \
            other.email == self.email and \
            other.street == self.street and \
            other.city == self.city and \
            other.state == self.state and \
            other.country == self.country and \
            other.post_code == self.post_code

    def __ne__(self, other):
        """Compare Person instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a Person"""
        return self.name + " " + self.email

    def __repr__(self):
        """Return an unambiguous String representation of a Person"""
        return "id={self.id},first_name='{self.first_name}',middles='{self.middles}'," \
               "last_name='{self.last_name}',email='{self.email}',street='{self.street}'," \
               "city='{self.city}',state='{self.state}',country='{self.country}'," \
               "post_code='{self.post_code}'".format(self=self)

    def from_json(self, json_dict):
        """
        Update a Person's attributes with new values.

        :param json_dict:
            Person's new attribute values.
        :type json_dict:
            dictionary
        """
        # In this class, because Address is a composite object, self.address is an
        # instance of SQLAlchemy InstanceState class, which magically passes certain
        # Person attributes through to a nested dictionary that holds Address attributes.
        # But we'll have to flatten the JSON value (which has a nested Address object)
        # so we can assign the Address attributes to the Person.
        json_copy = dict(json_dict)
        # First, deal with JSON null values
        json_sanitized = {k: (v if v is not None and v != 'null' else None)
                          for (k, v) in json_copy.items()}
        # Remove the Person's nested Address object
        address_json = json_copy.pop("address", None)
        # Flatten the JSON dictionary's nested Address member
        if address_json is not None:
            json_sanitized.update(**address_json)
        # Now assign all attributes to the Person
        self.__dict__.update(**json_sanitized)

    def __json__(self, request):
        """
        Return a JSON representation of the Person.

        This method is required for Pyramid to serialize Person to JSON
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middles": self.middles,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address
        }

# TODO: map subclasses to support polymorphic queries. See:
# https://groups.google.com/forum/#!topic/sqlalchemy/GJvbhXsxwuo
# http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#basic-control-of-which-tables-are-queried
