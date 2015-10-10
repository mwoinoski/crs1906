"""
Pyramid View Callable for requests related to user login.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
import transaction
import logging

# from .models import person_class
from ..models.person import Person
from ..models.persistence.person_dao import BaseDao

logger = logging.getLogger(__name__)


class LoginView:
    """View Callable for login processing"""

    def __init__(self, request, dao=BaseDao):
        """DAO dependency will be injected from dao arg"""
        self._request = request
        self._person_dao = dao()  # construct DAO instance and inject

    # URLs are mapped to route names in __init__.py with Configurator.add_route()

    # Pyramid calls this method for a request like this:
    # http://localhost:6543/
    #@view_config(route_name='index',
    #            renderer='../templates/index.pt')
    def index(self):
        return {}

    # Pyramid calls this method for a request like this:
    # http://localhost:6543/login_form
    #@view_config(route_name='login_form',
    #             renderer='../templates/login_form.pt')
    def login_form(self):
        return {}

    # Pyramid calls this method for a request like this:
    # http://localhost:6543/login?user_id=Homer&password=secret
    #@view_config(route_name='login',
    #             renderer='../templates/login_success.pt')
    def login(self):
        try:
            user_id = self._request.params['user_id']
            password = self._request.params['password']
            logger.debug("user_id = %s, password = %s", user_id, password)
            # FIXME: configure authentication
            person = self._person_dao.get_person(
                user_id, self._request.db_session)
            # person = self.request.db_session\
            #              .query(Person)\
            #              .filter(Person.first_name == user_id)\
            #              .first()
            logger.debug("person = %s", repr(person))
            # FIXME: query based on user_id instead of first_name
            result = {'user': person}
        except DBAPIError:
            msg = "There was a problem retrieving your information"
            result = Response(LoginView.error_msg.format(msg=msg),
                              content_type='text/html', status_int=500)
        except Exception as e:
            raise
            # msg = e.__class__.__name__ + ": " + ",".join(e.args)
            # result = Response(ViewCallable.error_msg.format(msg=msg),
            #                   content_type='text/html', status_int=500)
        return result

    error_msg = """\
        <html>
            <body>
                <h3>Uh-oh. Looks like there was a problem:</h3>
                <p>{msg}</p>
            </body>
        </html>
    """
