"""
Unit tests for UserServiceRest

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/testing.html
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from unittest.mock import MagicMock

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from ticketmanor.models.person import Person
from ticketmanor.rest_services.user_service import UserServiceRest
from ticketmanor.models.persistence.person_dao import BaseDao

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
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

        # For integration test, add model to in-memory DB
        # engine = create_engine('sqlite://')
        # DBSession.configure(bind=engine)
        # Base.metadata.create_all(engine)
        # with transaction.manager:
        #     DBSession.add(UserServiceRestTest.model)

    def tearDown(self):
        # DBSession.remove()
        testing.tearDown()

    def test_get_success(self):
        class StubDao:
            person = Person(id=123)
            get = \
                MagicMock(spec=BaseDao, return_value=person)
        request = testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=StubDao)

        result = user_service.get_user()

        self.assertEqual(result, StubDao.person)

    def test_get_not_found(self):
        class StubDao:
            get = MagicMock(side_effect=HTTPNotFound())
        request = testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=StubDao)

        with self.assertRaises(HTTPNotFound):
            user_service.get_user()

    def test_add_user_success(self):
        class StubDao:
            add = MagicMock(spec=BaseDao)
        request = testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=StubDao)

        response = user_service.add_user()

        self.assertEqual(201, response.status_int)

    def test_update_user_success(self):
        class StubDao:
            update = MagicMock(spec=BaseDao)
        request = testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=StubDao)

        response = user_service.update_user()

        self.assertEqual(202, response.status_int)

    def test_update_user_not_found(self):
        class StubDao:
            update = MagicMock(side_effect=HTTPNotFound())
        request = testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=StubDao)

        with self.assertRaises(HTTPNotFound):
            user_service.update_user()

    def test_delete_user_success(self):
        class StubDao:
            delete = MagicMock(spec=BaseDao)
        request = testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=StubDao)

        response = user_service.delete_user()

        self.assertEqual(202, response.status_int)

    def test_delete_user_not_found(self):
        class StubDao:
            delete = MagicMock(side_effect=HTTPNotFound())
        request = testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=StubDao)

        with self.assertRaises(HTTPNotFound):
            user_service.delete_user()

if __name__ == '__main__':
    main()
