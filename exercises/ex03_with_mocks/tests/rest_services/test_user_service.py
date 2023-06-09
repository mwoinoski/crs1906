"""
Unit tests for UserServiceRest

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/pyramid_testing.html
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest.mock import Mock
import pytest
from pytest import raises

from pyramid import testing as pyramid_testing
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from ticketmanor.models.person import Person
from ticketmanor.rest_services.user_service import UserServiceRest
from ticketmanor.models.persistence import PersistenceError
from ticketmanor.models.persistence.person_dao import PersonDao


class TestUserServiceRest:
    """Unit tests for Pyramid view callable UserServiceRest"""

    def test_get_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None

        # TODO: review the following test code and make sure you understand it
        #       (no code changes required)

        expected_result = Person(id=123)
        mock_dao = Mock(spec=PersonDao)
        mock_dao.get.return_value = expected_result
        user_service = UserServiceRest(None, request, mock_dao)

        actual_result = user_service.get_user('a@b.com')

        assert actual_result == expected_result

    def test_get_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None

        # TODO: create a mock DAO
        ....

        # TODO: assign None to the return value of the mock DAO's `get` method
        # HINT: see slide 3-38
        ....

        # TODO: create a UserServiceRest instance, passing the mock_dao as
        #       the third argument
        user_service = UserServiceRest(None, request, ....)

        # TODO: add a `with` statement to assert that the nested method call
        #       raises an HTTPNotFound exception
        with ....
            # TODO: call the UserServiceRest's `get_user` method, passing
            #       any string as an argument
            ....

    # TODO: After you get the first test case running, uncomment the following
    #       test case and make the required changes. Then run the file again and
    #       verify this second test case passes.

    # def test_get_user_dao_exception(self):
    #     request = pyramid_testing.DummyRequest()
    #     request.db_session = None
    #
    #     # TODO: create a mock DAO
    #     ....
    #
    #     # TODO: assign a PersistenceError as the side effect of
    #     #       the mock's `get` method
    #     # HINT: see slide 3-39
    #     ....
    #
    #     # TODO: create a UserServiceRest instance, passing the mock_dao as
    #     #       the last argument
    #     ....
    #
    #     # TODO: add a `with` statement to assert that the nested method call
    #     #       raises an HTTPNotFound exception
    #     ....
    #         # TODO: call the UserServiceRest's `get_user` method, passing
    #         #       any string as an argument
    #         ....

    def test_add_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock(spec=PersonDao))

        response = user_service.add_user()

        assert 201 == response.status_int

    def test_add_user_db_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        mock_dao = Mock(spec=PersonDao)
        mock_dao.add.side_effect = PersistenceError()
        user_service = UserServiceRest(None, request, mock_dao)

        with raises(HTTPInternalServerError, match=r'Could not add user'):
            user_service.add_user()

    def test_update_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock(spec=PersonDao))

        response = user_service.update_user()

        assert 202 == response.status_int

    def test_update_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        mock_dao = Mock(spec=PersonDao)
        mock_dao.update.side_effect = PersistenceError()
        user_service = UserServiceRest(None, request, mock_dao)

        with raises(HTTPNotFound):
            user_service.update_user()

    def test_delete_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock(spec=PersonDao))

        response = user_service.delete_user()

        assert 204 == response.status_int

    def test_delete_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        mock_dao = Mock(spec=PersonDao)
        mock_dao.delete.side_effect = PersistenceError()
        user_service = UserServiceRest(None, request, mock_dao)

        with raises(HTTPNotFound):
            user_service.delete_user()

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self):
        """ Called before and after each test case """

        # SETUP
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

        yield  # the test case will be called here

        # TEARDOWN
        # all code after `yield` will be executed after the test case
        pyramid_testing.tearDown()
