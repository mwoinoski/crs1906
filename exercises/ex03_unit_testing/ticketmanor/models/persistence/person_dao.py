"""
DAO for Person.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import logging
from ...models.person import Person
from .base_dao import BaseDao

logger = logging.getLogger(__name__)


# FIXME: should this be a mixin base class for Person,
#       so that Person manages its own persistence?
class PersonDao(BaseDao):
    """
    Persistence methods for Person instances.
    """

    def __init__(self):
        """Initialize the PersonDao"""
        super().__init__(Person, 'email')
