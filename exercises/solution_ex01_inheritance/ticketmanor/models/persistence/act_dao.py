"""
DAO for Act.
"""

from datetime import datetime, timedelta
from random import randint, randrange
import logging
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from ...util.utils import func_name
from ...models.act import Act
from .base_dao import BaseDao

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

logger = logging.getLogger(__name__)


# TODO: make the ActDao class a subclass of BaseDao
class ActDao(BaseDao):
    """
    Persistence methods for Act instances.
    """

    # TODO: define the __init__() method, with one parameter, self
    def __init__(self):
        """Initialize the ActDao"""
        super().__init__(Act, 'id')

    def query_for_act(self, db_session, *, act_type, search_type, **kwargs):
        """
        Search for an act of the given type.

        :param db_session a Session instance
        :param act_type music, sports, movie, or theater
        :param search_type based on act_type; e.g., music searches support
               searches for Artist, Venue, City, Date, and City
        Remaining keyword args are names of attributes of the Act class.
        Example: dao.query_for_act(
                     db_session,
                     act_type='music',
                     search_type='Artist',
                     title='Berlin Philharmonic')
        """
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
            raise ValueError(f'Unknown act type {act_type}')

        act = query.filter_by(**kwargs)\
                   .first()
        # TODO: should return all acts that match the query, not just the first
        #       (needs changes in concerts.html, movies.html, and sports.html)

        # TODO: get ticket price and images from DB, then delete the following
        if hasattr(act, 'events'):
            for event in act.events:
                event.price = ActDao.generate_price(event.venue.country)
                event.date_time = ActDao.generate_event_date_time()
                event.image_thumbnail = '/static/images/concerts-{}.png'\
                                        .format(randrange(1, 7))
                event.image_banner = '/static/images/concerts.jpg'

        return act

    @staticmethod
    def search_music(query, search_type, kwargs):
        """Does a search for music acts based on keyword arguments"""
        if search_type == 'Artist':
            if 'title' in kwargs.keys():
                like_str = "%{}%".format(kwargs.pop('title'))
                query = query.filter(or_(Act.title.like(like_str),
                                         Act.notes.like(like_str)))
        else:
            raise ValueError(f'No music search type "{search_type}"')
        return query

    @staticmethod
    def search_movie(query, search_type, kwargs):
        """Does a search for movies based on keyword arguments"""
        if search_type == 'Title':
            if 'title' in kwargs.keys():
                like_str = "%{}%".format(kwargs.pop('title'))
                query = query.filter(or_(Act.title.like(like_str),
                                         Act.notes.like(like_str)))
        else:
            raise ValueError(f'No movie search type "{search_type}"')
        return query

    @staticmethod
    def generate_price(country):
        symbol = '$' if country == 'USA' else '\u20AC'
        return symbol + str(randrange(60, 200, 5))

    @staticmethod
    def generate_event_date_time():
        return datetime.now().replace(hour=randint(19, 21), minute=0, second=0) + \
               timedelta(days=randint(1, 120))

    def get_act_and_events(self, act_id, db_session):
        """Eagerly loads the act and associated events for a given act id"""
        logger.debug("%s: act_id = %s", func_name(self), act_id)

        act = db_session.query(Act)\
                        .options(joinedload(Act.events))\
                        .filter_by(id=act_id).one()
        return act
