"""
Unit tests for UserServiceRest

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/pyramid_testing.html
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from unittest.mock import Mock, ANY
import sqlite3

from pyramid import testing as pyramid_testing
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from ticketmanor.models.person import Person
from ticketmanor.rest_services.user_service import UserServiceRest
from ticketmanor.models.persistence import PersistenceError

# import transaction
# from sqlalchemy import create_engine
# from ticketmanor.models import DBSession, Base


class UserServiceRestTest:
    """Unit tests for Pyramid view callable UserServiceRest"""

    def setUp(self):
        # Create a Pyramid test environment that has an isolated registry and 
        # an isolated request for the duration of a single test. Each call to
        # get_current_registry() within a test case method will return the
        # application registry associated with the config Configurator instance
        request = pyramid_testing.DummyRequest()
        self.config = pyramid_testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

        # For integration test, add the model to the in-memory DB
        # engine = create_engine('sqlite://')
        # DBSession.configure(bind=engine)
        # Base.metadata.create_all(engine)
        # with transaction.manager:
        #     DBSession.add(UserServiceRestTest.model)

    def tearDown(self):
        # DBSession.remove()
        pyramid_testing.tearDown()

    def test_get_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        #request.matchdict['email'] = 'benf@gmail.com'
        
        expected_result = Person(id=123)
        mock_dao = Mock()
        mock_dao.get.return_value = expected_result
        user_service = UserServiceRest(None, request, mock_dao)
        #user_service = UserServiceRest(None, request, dao=Mock)
        #user_service._dao.get.return_value = expected_result

        actual_result = user_service.get_user('a@b.com')
        #actual_result = user_service.get_user_json()

        self.assertEqual(actual_result, expected_result)

    def test_get_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        #request.matchdict['email'] = 'nobody@gmail.com'
        
        # TODO: create a mock DAO
        mock_dao = Mock()

        # TODO: assign None to the return value of the mock's `get` method
        # HINT: see slide 3-38
        mock_dao.get.return_value = None

        # TODO: create a UserServiceRest instance, passing the mock_dao as
        #       the last argument
        user_service = UserServiceRest(None, request, mock_dao)
        #user_service = UserServiceRest(None, request, dao=Mock)
        #user_service._dao.get = Mock(side_effect=PersistenceError())

        # TODO: add a `with` statement to assert that the nested method call
        #       raises an HTTPNotFound exception
        with raises(HTTPNotFound):
        #with self.assertRaises(HTTPNotFound):
            # TODO: call the UserServiceRest's `get_user` method, passing
            #       any string as an argument
            user_service.get_user('a@b.com')
            #user_service.get_user_json()

    def test_get_user_dao_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        #request.matchdict['email'] = 'nobody@gmail.com'
        
        # TODO: create a mock DAO
        mock_dao = Mock()
        
        # TODO: assign a sqlite3.Error as the side effect of 
        #       the mock's `get` method
        # HINT: see slide 3-39
        mock_dao.get.side_effect = sqlite3.Error('SQL error')
        
        # TODO: create a UserServiceRest instance, passing the mock_dao as
        #       the last argument
        user_service = UserServiceRest(None, request, mock_dao)
        #user_service = UserServiceRest(None, request, dao=Mock)
        #user_service._dao.get = Mock(side_effect=ValueError())

        # TODO: add a `with` statement to assert that the nested method call
        #       raises an HTTPNotFound exception
        with raises(HTTPNotFound):
        #with self.assertRaises(ValueError):
            # TODO: call the UserServiceRest's `get_user` method, passing
            #       any string as an argument
            user_service.get_user('a@b.com')
            #user_service.get_user_json()

    def test_add_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)

        response = user_service.add_user()

        self.assertEqual(201, response.status_int)

    def test_add_user_db_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)
        user_service._dao.add = Mock(side_effect=sqlite3.DatabaseError())

        with self.assertRaisesRegex(HTTPInternalServerError, r'Could not add'):
            user_service.add_user()
        user_service._dao.add.assert_called_with(ANY, ANY)

    def test_update_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)

        response = user_service.update_user()

        self.assertEqual(202, response.status_int)

    def test_update_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)
        user_service._dao.update = Mock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.update_user()

    def test_delete_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock)

        response = user_service.delete_user()

        self.assertEqual(204, response.status_int)

    def test_delete_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock)
        user_service._dao.delete = Mock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.delete_user()

if __name__ == '__main__':
    main()
