"""
business_object.py - Classes for exercising mock objects
"""

import sqlite3


class BusinessObject:
    """Simple class for mock demo"""

    def __init__(self, name=''):
        self.name = name
        self.user_dao = UserDao()

    def get_user(self, user_id):
        try:
            user = self.user_dao.query_user(user_id)
            if user is None:
                raise ValueError('{} is not a valid user ID'.format(user_id))

            return user
        except sqlite3.Error as e:
            raise BusinessError('Problem fetching user with ID {}: {}'
                                .format(user_id, str(e)))

    def __str__(self):
        return "{self.name}".format(self=self)


class UserDao(object):
    """Class that encapsulates database access"""
    def __init__(self):
        pass  # Production DAO would create connection to database

    def query_user(self, user_id):
        return Person(123, 'Isaac', None, 'Newton')
        # Production DAO would query database for user by ID


class BusinessError(Exception):
    """Application-specific exception class"""
    def __init__(self, msg):
        super().__init__(msg)


class Person:
    """Simple class for testing mock objects"""
    def __init__(self, user_id, first_name, middle_name, last_name):
        self.id = user_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def __str__(self):
        return "{self.id} {self.first_name} {self.middle_name} {self.last_name}"\
            .format(self=self)
