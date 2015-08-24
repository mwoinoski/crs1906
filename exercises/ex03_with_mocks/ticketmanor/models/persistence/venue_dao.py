"""
DAO for Venue.
"""
from sqlalchemy.orm import joinedload
from ticketmanor.models.persistence import PersistenceError
from ticketmanor.models.persistence.base_dao import BaseDao

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import logging
from ...util.utils import func_name
from ...models.venue import Venue

logger = logging.getLogger(__name__)


class VenueDao(BaseDao):
    """
    Persistence methods for Venue instances.
    """

    def __init__(self):
        """Initialize a VenueDao"""
        super().__init__(Venue, 'id')

    @classmethod
    def get_venue_by_name(cls, venue_name, db_session):
        """Looks up a venue by name"""
        logger.debug("%s: venue_name = %s", func_name(cls), venue_name)
        venue = db_session.query(Venue)\
                          .filter_by(name=venue_name)\
                          .first()
        return venue

    @classmethod
    def get_venue_and_events(cls, venue_id, db_session):
        """
        Eagerly loads the venue and associated events for a given venue id
        """
        logger.debug("%s: venue_name = %s", func_name(cls), venue_id)
        venue = db_session.query(Venue)\
                          .options(joinedload(Venue.events))\
                          .filter_by(id=venue_id).one()
        return venue
