"""
Pyramid View Callable for requests related to adding a user.
"""

__author__ = 'Mike Woinoski mike@articulatedesign.us.com'

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
import transaction
import logging

# from .models import person_class
from ..models.person import Person
from ..models.persistence.person_dao import BaseDao

logger = logging.getLogger(__name__)


class AddUserView:
    def __init__(self, request, dao=BaseDao):
        """DAO dependency will be injected from dao arg"""
        self._request = request
        self._person_dao = dao()  # construct DAO instance and inject

    # URLs are mapped to route names in __init__.py with Configurator.add_route()

    # Pyramid calls this method for a request like this:
    # http://localhost:6543/add_user_form
    #@view_config(route_name='add_user_form',
    #             renderer='../templates/add_user_form.pt')
    def add_user_form(self):
        return {}

    # Pyramid calls this method for a request like this:
    # http://localhost:6543/add_member?first_name=Homer&last_name=Simpson&nick_name=Homie
    #@view_config(route_name='add_user',
    #             renderer='../templates/add_user_success.pt')
    def add_user(self):
        try:
            with transaction.manager:
                # TODO: persist password and user_id
                person = Person(
                    first_name=self._request.params['first_name'],
                    middles=self._request.params['middles'],
                    last_name=self._request.params['last_name'],
                    email=self._request.params['email'],
                    street=self._request.params['street'],
                    city=self._request.params['city'],
                    state=self._request.params['state'],
                    country=self._request.params['country'],
                    post_code=self._request.params['post_code']
                )
                self._request.db_session.add(person)
                result = {'user': person}
        except DBAPIError:
            msg = "Couldn't add user " + \
                  person.name + " " if person is not None else "" +\
                  "to DB"
            result = Response(AddUserView.error_msg.format(msg=msg),
                              content_type='text/html', status_int=500)
        except Exception as e:
            msg = e.__class__.__name__ + ": " + ",".join(e.args)
            result = Response(AddUserView.error_msg.format(msg=msg),
                              content_type='text/html', status_int=500)
        return result

    error_msg = """\
        <html>
            <body>
                <h3>Uh-oh. Looks like there was a problem:</h3>
                <p>{msg}</p>
            </body>
        </html>
    """
