"""
user_dao.py - Classes for exercising mock objects
"""

from person import Person


class UserDao(object):
    """Class that encapsulates database access"""

    def __init__(self):
        print('UserDao.__init__')
        pass  # Production DAO would create connection to database

    def query_user(self, user_id):
        print('UserDao.query_user({})'.format(user_id))
        return Person('Isaac', None, 'Newton')
        # Production DAO would query database for user by ID
