"""
Unit tests for UserServiceRest

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/pyramid_testing.html
"""

from unittest import TestCase, main
from unittest.mock import Mock, ANY
import sqlite3

from pyramid import testing as pyramid_testing
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from ticketmanor.models.person import Person
from ticketmanor.rest_services.user_service import UserServiceRest
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


class UserServiceRestTest(TestCase):
    """Unit tests for Pyramid view callable UserServiceRest"""

    def setUp(self):
        # Set up for Pyramid web application framework.
        request = pyramid_testing.DummyRequest()
        self.config = pyramid_testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        pyramid_testing.tearDown()

    def test_get_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'

        # TODO: note that we pass Mock as the DAO class to the
        #       UserServiceRest constructor.
        #       (no code change required)
        user_service = UserServiceRest(None, request, dao=Mock)

        person = Person(id=123)

        # TODO: note how we access the DAO from the UserServiceRest instance
        #       after the Mock DAO has been set. Here, we program the Mock so that
        #       its get() method returns a reference to the Person created above.
        #       (no code change required)
        user_service._dao.get.return_value = person

        result = user_service.get_user('benf@gmail.com')

        self.assertEqual(result, person)

    def test_get_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'

        # TODO: pass Mock as the DAO class to the UserServiceRest constructor.
        # HINT: in the following statement, change the `dao` keyword argument 
        #       from None to the appropriate value
        user_service = UserServiceRest(None, request, dao=None)

        # TODO: configure the mock so that a call to its get() method has
        #       the side effect of raising a PersistenceError
        # HINT: see slide 3-39
        

        # TODO: assert that an HTTPNotFound exception is raised when you call
        #       the user_service's get_user() method.
        # HINT: see slide 3-38
        

    def test_get_unhandled_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'

        # TODO: pass Mock as the DAO class to the UserServiceRest constructor.
        user_service = UserServiceRest(None, request, dao=None)

        # TODO: program the mock DAO's get() method to have a side effect of
        # raising a ValueError.
        

        # TODO: assert that a ValueError is raised when you call
        #       the user_service's get_user() method.
        

    def test_get_user_PersistenceError(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock)

        # TODO: program the mock DAO's get() method to have a side effect of
        #       raising a PersistenceError.
        

        # TODO: assert that an HTTPNotFound is raised when you call
        #       the user_service's get_user() method.
        

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

        # TODO: note the mock DAO's add() method will raise a DatabaseError.
        #       (no code change required)
        user_service._dao.add = Mock(side_effect=sqlite3.DatabaseError())

        # TODO: assert that an HTTPInternalServerError is raised when you call
        #       the user_service's add_user() method, and that the exception's
        #       message includes the string 'Could not add'
        # HINT: see slide 3-39
        

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
