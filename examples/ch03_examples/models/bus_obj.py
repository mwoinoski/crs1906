"""
business_object.py - Classes for exercising mock objects
"""

import sqlite3
from db.user_dao import UserDao


class BusinessObject:
    """Simple class for mock demo"""

    def __init__(self, name=''):
        print('BusinessObject.__init__')
        self.name = name
        self.user_dao = UserDao()

    def get_user(self, user_id):
        try:
            user = self.user_dao.query_user(user_id)

            print('BusinessObject.get_user: user_dao.query_user returned '
                  'user ' + user.last_name if user else None)

            if user is None:
                raise ValueError('{} is not a valid user ID'.format(user_id))

            return user
        except sqlite3.Error as e:
            raise BusinessError('Problem fetching user with ID {}: {}'
                                .format(user_id, str(e)))

    def __str__(self):
        return "{self.name}".format(self=self)


class BusinessError(Exception):
    """Application-specific exception class"""
    def __init__(self, msg):
        super().__init__(msg)
