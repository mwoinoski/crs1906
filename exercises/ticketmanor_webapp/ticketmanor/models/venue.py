"""
Venue model class
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
)
from sqlalchemy.orm import relationship
from . import Base


class Venue(Base):
    """
    Model class for Venue
    """
    __tablename__ = 'venues'
    id = Column('id', Integer, primary_key=True)  # autoincrement=True by default
    name = Column('name', String)
    street_address = Column('streetAddress', String)
    city = Column('city', String)
    prov_state = Column('provState', String)
    country = Column('country', String)
    latitude = Column('lat', Float)
    longitude = Column('lng', Float)
    # Venue has a bidirectional one-to-many relationship with Event.
    # The relationship is fully mapped in the Event class and does
    # not need to be mapped here.
    # To map one-to-one, use this: relationship('Event', uselist=False, backref='venue')

    def __eq__(self, other):
        """Compare Person instances."""
        # Because the Person's Address is declared as a composite,
        # you must compare the address attributes of the Persons.
        # Don't delegate the address comparison to
        # Address.__eq__(), because SQLAlchemy may create a
        # dictionary to hold the values rather than an Address.
        return isinstance(other, Venue) and \
            other.id == self.id and \
            other.name == self.name and \
            other.street_address == self.street_address and \
            other.city == self.city and \
            other.prov_state == self.prov_state and \
            other.country == self.country and \
            other.latitude == self.latitude and \
            other.longitute == self.longitude

    def __ne__(self, other):
        """Compare Venue instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a Venue"""
        return "{self.id} {self.name} {self.street_address} {self.prov_state} " \
               "{self.country} {self.latitude} {self.longitude}".format(self=self)

    def __repr__(self):
        """Return an unambiguous String representation of a Venue"""
        return "id={self.id},name='{self.name}',street_address='{self.street_address}'," \
               "city='{self.city}',prov_state='{self.prov_state}',country='{self.country}'," \
               "latitude='{self.latitude}',longitude='{self.longitude}'".format(self=self)

    def __json__(self):
        """
        Return a dictionary that can be mapped to a JSON representation of
        the Venue.

        This method is required for Pyramid to serialize Venue to JSON
        """
        # Don't return self.__dict__: SQLAlchemy adds extra data attributes
        return {
            "id": self.id,
            "name": self.name,
            "street_address": self.street_address,
            "city": self.city,
            "prov_state": self.prov_state,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
