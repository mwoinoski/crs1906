"""
Unit tests for Pyramid view callable LoginView

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/testing.html
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from unittest.mock import MagicMock

from pyramid import testing

from ticketmanor.models.person import Person
from ticketmanor.views.login_view import LoginView
from ticketmanor.models.persistence.person_dao import BaseDao

# import transaction
# from sqlalchemy import create_engine
# from ticketmanor.models import DBSession, Base

class LoginViewTest(TestCase):
    """Unit tests for Pyramid view callable LoginView"""

    model = None

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
        #     DBSession.add(LoginViewTest.model)

        LoginViewTest.model = Person(id=6, first_name='Ben', last_name='Franklin')

    def tearDown(self):
        # DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        class StubDao:
            person = Person(id=123)
            get_person = \
                MagicMock(spec=BaseDao, return_value=person)
        request = testing.DummyRequest()
        request.db_session = None
        request.params['user_id'] = 'Ben'
        request.params['password'] = 'lightning'
        login_view = LoginView(request, dao=StubDao)

        result = login_view.login()

        self.assertEqual(result['user'], StubDao.person)

    def test_failing_view_DBAPIError(self):
        class StubDao:
            from sqlalchemy.exc import DBAPIError
            get_person = \
                MagicMock(side_effect=DBAPIError('DB error', None, None))
        request = testing.DummyRequest()
        request.db_session = None
        request.params['user_id'] = 'Ben'
        request.params['password'] = 'lightning'
        login_view = LoginView(request, dao=StubDao)

        result = login_view.login()

        self.assertEqual(result.status_int, 500)

if __name__ == '__main__':
    main()
