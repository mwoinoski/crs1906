"""
DAO for Venue.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from sqlalchemy.orm import joinedload

from ticketmanor.models.persistence import PersistenceError
from ticketmanor.models.persistence.base_dao import BaseDao
from ticketmanor.models.persistence import PersistenceError
from ticketmanor.models.venue import Venue


# TODO: make the VenueDao class a subclass of BaseDao
class VenueDao:
    """
    Persistence methods for Venue instances.
    """

    # TODO: define the __init__() method, with one parameter, self

        # TODO: in the __init__() method, call the superclass's __init__(),
        # passing two arguments:
        # 1. the class of the entity that will be persisted (Venue)
        # 2. the name of the entity's ID field ('id')


    @classmethod
    def get_venue_by_name(cls, venue_name, db_session):
        """Looks up a venue by name"""
        venue = db_session.query(Venue)\
                          .filter_by(name=venue_name)\
                          .first()
        return venue

    @classmethod
    def get_venue_and_events(cls, venue_id, db_session):
        """
        Eagerly loads the venue and associated events for a given venue id
        """
        venue = db_session.query(Venue)\
                          .options(joinedload(Venue.events))\
                          .filter_by(id=venue_id).one()
        return venue

    # TODO: Note that the following methods are the same as the methods that
    # you pasted into the BaseDao class.

    # TODO: delete all the methods below this comment.

    def get(self, id_value, db_session):
        entity = db_session.query(Venue)\
                           .filter(getattr(Venue, 'id') == id_value)\
                           .first()
        return entity

    def add(self, entity, db_session):
        db_session.add(entity)

    def update(self, entity, db_session):
        db_session.merge(entity)

    def delete(self, id_value, db_session):
        entity = self.get(id_value, db_session)
        if entity:
            db_session.delete(entity)
        else:
            raise PersistenceError('No entity with ID {} found'
                                   .format(id_value))
