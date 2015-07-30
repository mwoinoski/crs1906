"""
DAO for Act.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import logging
import random
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from ...util.utils import func_name
from ...models.act import Act
from .base_dao import BaseDao

logger = logging.getLogger(__name__)


class ActDao(BaseDao):
    """
    Persistence methods for Act instances.
    """

    def __init__(self):
        super().__init__(Act, 'id')

    def query_for_act(self, db_session, search_type, **kwargs):
        """Search for an act of the given type and title.

           Keyword args are names of attributes of Act class.
           Example: dao.query_for_act(
                        db_session,
                        search_type='Artist',
                        title='London Symphony')"""
        logger.debug("%s: args = %s, %s", func_name(self), search_type,
                     ','.join(['{}={}'.format(k, kwargs[k]) for k in kwargs]))

        query = db_session.query(Act).filter_by(act_type=kwargs.pop('act_type'))
        if 'title' in kwargs.keys():
            like_str = "%{}%".format(kwargs.pop('title'))
            query = query.filter(or_(Act.title.like(like_str),
                                     Act.notes.like(like_str)))
        act = query.filter_by(**kwargs)\
                   .first()
        # TODO: return all acts that match the query, not just the first
        #       (needs changes in concerts.html, movies.html, and sports.html)

        # TODO: get ticket price and images from DB, then delete the following
        if hasattr(act, 'events'):
            for event in act.events:
                event.price = self.generate_price(event.venue.country)
                event.image_thumbnail = '/static/images/concerts-{}.png'\
                                            .format(random.randrange(1, 7))
                event.image_banner = '/static/images/concerts.jpg'

        return act

    def generate_price(self, country):  # TODO: delete when DB is complete
        symbol = '$' if country == 'USA' else '\u20AC'
        return symbol + str(random.randrange(60, 200, 5))

    def get_act_and_events(self, id, db_session):
        """Eagerly loads the act and associated events for a given act id"""
        logger.debug("%s: id = %s", func_name(self), id)

        act = db_session.query(Act)\
                        .options(joinedload(Act.events))\
                        .filter_by(id=id).one()
        return act
