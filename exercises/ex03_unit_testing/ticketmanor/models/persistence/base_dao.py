"""
BaseDao is the base class for DAOs for all entities.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import logging
from ...util.utils import func_name
from ticketmanor.models.persistence import PersistenceError

logger = logging.getLogger(__name__)


class BaseDao:
    """
    Base class for DAOs for all entities.
    """

    def __init__(self, entity_class, id_attr):
        self._entity_class = entity_class
        self._id_attr = id_attr

    def get(self, id_value, db_session):
        logger.debug("%s: get %s %s = %s", func_name(self),
                     self._entity_class.__class__.__name__,
                     self._id_attr, id_value)
        entity = db_session.query(self._entity_class)\
                           .filter(getattr(self._entity_class,
                                           self._id_attr) == id_value)\
                           .first()
        # Example filter query: .filter(Person.email == id_value)
        if not entity:
            raise PersistenceError(
                "Can't get {} with id {}: not in database"
                .format(self._entity_class.__name__, id_value))
        #  Simple fetch by primary key: act = db_session.query(Act).get(act_id)
        return entity

    def add(self, entity, db_session):
        logger.debug("%s: add %s %s", func_name(self),
                     entity.__class__.__name__, repr(entity))
        db_session.add(entity)
        logger.debug("%s: added %s %s", func_name(self),
                     entity.__class__.__name__, repr(entity))

    def update(self, entity, db_session):
        logger.debug("%s: update %s %s", func_name(self),
                     entity.__class__.__name__, repr(entity))
        db_session.merge(entity)
        logger.debug("%s: updated %s %s", func_name(self),
                     entity.__class__.__name__, repr(entity))

    def delete(self, id_value, db_session):
        logger.debug("%s: delete %s %s = %s", func_name(self),
                     self._entity_class.__name__, self._id_attr, id_value)
        # We need to make sure we don't call the subclass's get method,
        # so we'll explicitly call the base class definition.
        entity = BaseDao.get(self, id_value, db_session)
        db_session.delete(entity)
        logger.debug("%s: deleted %s %s", func_name(self),
                     self._entity_class.__name__, repr(entity))
