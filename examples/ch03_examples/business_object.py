r"""
business_object.py - Classes for exercising mock objects
"""

import sqlite3


class BusinessObject:
    """Simple class for mock demo"""

    def __init__(self, name=''):
        print('BusinessObject.__init__')
        self.name = name
        self.user_dao = UserDao()

    def get_user(self, user_id):
        try:
            user = self.user_dao.query_user(user_id)

            print('BusinessObject.get_user: user_dao.query_user returned user '
                  + user.last_name if user else None)

            if user is None:
                raise ValueError(f'{user_id} is not a valid user ID')

            return user
        except sqlite3.Error as e:
            raise BusinessError(
                f'Problem fetching user with ID {user_id}: {str(e)}')

    def __str__(self):
        return self.name


class UserDao(object):
    """Class that encapsulates database access"""
    def __init__(self):
        print('UserDao.__init__')
        pass  # Production DAO would create connection to database

    def query_user(self, user_id):
        print(f'UserDao.query_user({user_id})')
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
        return f"{self.id} {self.first_name} {self.middle_name} {self.last_name}"
