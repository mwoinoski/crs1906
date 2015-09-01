"""
BaseDao is the base class for DAOs for all entities.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'
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
