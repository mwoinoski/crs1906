"""
BaseDao is the base class for DAOs for all entities.
"""

from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


class BaseDao:
    """Base class for DAOs for all entities."""

    # TODO: note the definition of the BaseDao __init__ method().
    # Its three parameters are:
    # 1. the current DAO instance
    # 2. the class of the entity that this DAO can persist
    # 3. the name of the ID attribute of the persistent entity
    # (no code changes required)
    def __init__(self, entity_class, id_attr):
        self._entity_class = entity_class
        self._id_attr = id_attr

    # TODO: paste the methods from PersonDao here

    def get(self, id_value, db_session):
        # TODO: in the next statement, make the following changes:
        # 1. replace Person with the value of the DAO's _entity_class attribute
        #    (note: there are 2 occurrences of Person)
        # 2. replace 'email' with the value of the DAO's _id_attr attribute
        entity = db_session.query(self._entity_class)\
                           .filter(getattr(self._entity_class,
                                           self._id_attr) == id_value)\
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
