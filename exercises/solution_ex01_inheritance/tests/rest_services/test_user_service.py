"""
Unit tests for UserServiceRest

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/pyramid_testing.html
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from unittest.mock import MagicMock, ANY
import sqlite3

from pyramid import testing as pyramid_testing
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from ticketmanor.models.person import Person
from ticketmanor.rest_services.user_service import UserServiceRest
from ticketmanor.models.persistence import PersistenceError

# import transaction
# from sqlalchemy import create_engine
# from ticketmanor.models import DBSession, Base


class UserServiceRestTest(TestCase):
    """Unit tests for Pyramid view callable UserServiceRest"""

    def setUp(self):
        # environment that has an isolated registry and an isolated
        # request for the duration of a single test. Each call to
        #  get_current_registry() within a test case method will return
        # the application registry associated with the config
        # Configurator instance.
        request = pyramid_testing.DummyRequest()
        self.config = pyramid_testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

        # For integration test, add model to in-memory DB
        # engine = create_engine('sqlite://')
        # DBSession.configure(bind=engine)
        # Base.metadata.create_all(engine)
        # with transaction.manager:
        #     DBSession.add(UserServiceRestTest.model)

    def tearDown(self):
        # DBSession.remove()
        pyramid_testing.tearDown()

    def test_get_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=MagicMock)
        person = Person(id=123)
        user_service._dao.get.return_value = person

        result = user_service.get_user()

        self.assertEqual(result, person)

    def test_get_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=MagicMock)
        user_service._dao.get = MagicMock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.get_user()

    def test_get_unhandled_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=MagicMock)
        user_service._dao.get = MagicMock(side_effect=ValueError())

        with self.assertRaises(ValueError):
            user_service.get_user()

    def test_add_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=MagicMock)

        response = user_service.add_user()

        self.assertEqual(201, response.status_int)

    def test_add_user_db_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=MagicMock)
        user_service._dao.add = MagicMock(side_effect=sqlite3.DatabaseError())

        with self.assertRaisesRegex(HTTPInternalServerError, r'Could not add'):
            user_service.add_user()
        user_service._dao.add.assert_called_with(ANY, ANY)

    def test_update_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=MagicMock)

        response = user_service.update_user()

        self.assertEqual(202, response.status_int)

    def test_update_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=MagicMock)
        user_service._dao.update = MagicMock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.update_user()

    def test_delete_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=MagicMock)

        response = user_service.delete_user()

        self.assertEqual(202, response.status_int)

    def test_delete_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=MagicMock)
        user_service._dao.delete = MagicMock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.delete_user()

if __name__ == '__main__':
    main()
