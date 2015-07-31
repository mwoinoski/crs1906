"""
Act model class
"""

import json

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship, backref

from . import Base
from .event import Event

acts_events_join_table = Table('acts_events', Base.metadata,
    Column('acts_id', Integer, ForeignKey('acts.id')),
    Column('events_id', Integer, ForeignKey('events.id'))
)


class Act(Base):
    """
    Model class for Act
    """
    __tablename__ = 'acts'
    id = Column('id', Integer, primary_key=True)  # autoincrement=True by default
    title = Column('title', String)
    act_type = Column('type', Integer)  # {0: 'movies', 1: 'music', 2: 'theater', 3: 'sports'}
    year = Column('year', Integer)
    notes = Column('notes', String)
    events = relationship('Event',
                          order_by=Event.date_time,
                          secondary=acts_events_join_table,
                          backref=backref('acts', order_by='Act.id'))

    # Constants for Act type
    # BONUS TODO: Python 3.4 supports enums. Replace the following class
    # attributes with an enum named ActType.
    MOVIE = 0
    MUSIC = 1
    THEATER = 2
    SPORTS = 3
    # from enum import Enum
    # class ActType(Enum):
    #     movie = 0
    #     music = 1
    #     theater = 2
    #     sports = 3
    # act_type = ActType.music.value  # get int value of enum: 1
    # int_value = 1
    # act_enum = ActType(int_value)   # get enum from int: ActType.music

    # Dictionary to map act type int values to strings
    ACT_TYPE = {
        MOVIE: 'movie',
        MUSIC: 'music',
        THEATER: 'theater',
        SPORTS: 'sports',
    }

    # Dictionary for reverse lookups of act types (strings to ints)
    # BONUS TODO: replace the following loop with a dictionary comprehension
    # HINT: first, modify the for loop to use the dict items() method
    ACT_TYPE_INV = {v: k for k, v in ACT_TYPE.items()}
    # ACT_TYPE_INV = {}
    # for k in ACT_TYPE:
    #     v = ACT_TYPE[k]
    #     ACT_TYPE_INV[v] = k

    def __eq__(self, other):
        """Compare Act instances."""
        return isinstance(other, Act) and \
            other.id == self.id and \
            other.title == self.title and \
            other.act_type == self.act_type and \
            other.notes == self.notes

    def __ne__(self, other):
        """Compare Act instances."""
        return not self.__eq__(other)

    def __str__(self):
        """Return a human-readable representation of a Venue"""
        return "{self.id} {self.title} {act_type} {self.year} {self.notes}"\
            .format(act_type=Act.ACT_TYPE[self.act_type], self=self)

    def __repr__(self):
        """Return an unambiguous String representation of a Act"""
        return "id={self.id},title='{self.title}',act_type='{self.act_type}'," \
               "year='{self.year}',notes='{self.notes}'".format(self=self)

    def __json__(self, request=None):
        """
        Return a dictionary that can be mapped to a JSON representation of
        the Act.

        This method is required for Pyramid to serialize Act to JSON
        """
        act_json = {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "act_type": self.ACT_TYPE[self.act_type],
            "year": self.year,
            "events": [] if not hasattr(self, 'events')
                      else [event.__json__() for event in self.events],
        }
        return act_json
