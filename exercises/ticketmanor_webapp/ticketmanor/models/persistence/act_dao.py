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

    def query_for_act(self, db_session, *, act_type, search_type, **kwargs):
        """Search for an act of the given type.

           :param act_type music, sports, movie, or theater
           :param search_type based on act_type; e.g., music searches support
                  searches for Artist, Venue, City, Date, and City
           Remaining keyword args are names of attributes of the Act class.
           Example: dao.query_for_act(
                        db_session,
                        act_type='music',
                        search_type='Artist',
                        title='Berlin Philharmonic')"""
        logger.debug("%s: args = %s, %s", func_name(self), search_type,
                     ','.join(['{}={}'.format(k, kwargs[k]) for k in kwargs]))

        act_type_int = Act.ACT_TYPE_INV[act_type]  # convert string to int
        query = db_session.query(Act).filter_by(act_type=act_type_int)

        if act_type_int == Act.MUSIC:
            # Don't unwrap kwargs because the called method gets a copy of
            # kwargs and won't be able to pop items off the original kwargs
            query = ActDao.search_music(query, search_type, kwargs)

        elif act_type_int == Act.MOVIE:
            query = ActDao.search_movie(query, search_type, kwargs)

        elif act_type_int == Act.SPORTS:
            raise ValueError("Sports search function isn't implemented yet")

        else:
            raise ValueError('Unknown act type {}'.format(act_type))

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

    @staticmethod
    def search_music(query, search_type, kwargs):
        if search_type == 'Artist':
            if 'title' in kwargs.keys():
                like_str = "%{}%".format(kwargs.pop('title'))
                query = query.filter(or_(Act.title.like(like_str),
                                         Act.notes.like(like_str)))
        else:
            raise ValueError('No music search type "{}"'.format(search_type))
        return query

    @staticmethod
    def search_movie(query, search_type, kwargs):
        if search_type == 'Title':
            if 'title' in kwargs.keys():
                like_str = "%{}%".format(kwargs.pop('title'))
                query = query.filter(or_(Act.title.like(like_str),
                                         Act.notes.like(like_str)))
        else:
            raise ValueError('No movie search type "{}"'.format(search_type))
        return query

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
