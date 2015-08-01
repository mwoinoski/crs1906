"""
Event model class
"""
import json
from sqlalchemy.orm import relationship, backref

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
)
from . import Base
import time


class Event(Base):
    """
    Model class for Event
    """
    __tablename__ = 'events'
    id = Column('id', Integer, primary_key=True)  # default autoincrement=True
    date_time = Column('date_time', DateTime)
    # Define a bidirectional many-to-one relationship with Venue.
    venue_id = Column(Integer, ForeignKey('venues.id'))
    venue = relationship('Venue',
                         backref=backref('events', order_by='Event.id'))
    # To map a one-to-one relationship, set uselist=False:
    # venue = relationship('Venue', backref=backref('events', uselist=False))

    # TODO: schema defines column what_id as FK to act, but acts_events table
    #       defines the many-to-many relationship between Event and Act, so
    #       ignore the what_id column

    def __eq__(self, other):
        """Compare Event instances."""
        return isinstance(other, self.__class__) and \
            other.id == self.id and \
            other.date_time == self.date_time and \
            other.venue_id == self.venue_id

    def __ne__(self, other):
        """Compare Event instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a Venue"""
        return "{self.id} {self.date_time} {self.venue_id}".format(self=self)

    def __repr__(self):
        """Return an unambiguous String representation of a Event"""
        return "id={self.id},date_time='{self.date_time}'," \
               "venue_id='{self.venue_id}'".format(self=self)

    def __json__(self, request=None):
        """
        Return a dictionary that can be mapped to a JSON representation of
        the Event.

        This method is required for Pyramid to serialize Event to JSON
        """
        return {
            "id": self.id,
            "venue": self.venue.__json__() if hasattr(self, 'venue') else None,
            "date_time": self.date_time.timestamp(),
            "price": self.price,
            "image_thumbnail": self.image_thumbnail,
            "image_banner": self.image_banner,
            # If date_time is a string, do this instead:
            # "date_time": time.mktime(
            #     time.strptime(self.date_time, '%Y-%m-%d %H:%M:%S'))
        }

    def __hash__(self):
        return self.id
