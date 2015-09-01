"""
DAO for Person.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from ...models.person import Person
from .base_dao import BaseDao
from ticketmanor.models.persistence import PersistenceError


# TODO: make the PersonDao class a subclass of BaseDao
class PersonDao:
    """
    Persistence methods for Person instances.
    """

    # TODO: define the __init__() method, with one parameter, self
    def ...
        # TODO: call the superclass's __init__(), passing two arguments:
        # 1. the class of the entity that will be persisted (Person)
        # 2. the name of the entity's ID field ('email')
        super().__init__(...)

    # TODO: cut all methods from here to the end of the file and paste them
    # at the end of base_dao.py

    def get(self, id_value, db_session):
        # TODO: in the next statement, make the following changes:
        # 1. replace Person with the value of the DAO's _entity_class attribute
        #    (note that there are 2 occurrences of Person)
        # 2. replace 'email' with the value of the DAO's _id_attr attribute
        entity = db_session.query(Person)\
                           .filter(getattr(Person, 'email') == id_value)\
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
