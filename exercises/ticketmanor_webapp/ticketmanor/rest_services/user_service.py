"""
Pyramid View Callable for requests related to user management.
"""
import json
from pyramid.response import Response
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from pyramid.view import view_config, notfound_view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError
import logging
import re
from ..util.utils import func_name
from ..models.persistence.person_dao import PersonDao
from ..models.person import Person

logger = logging.getLogger(__name__)


@view_defaults(renderer='json')
class UserServiceRest:
    """View Callable for managing users"""

    def __init__(self, context, request, dao=PersonDao):
        """DAO dependency will be injected from dao arg"""
        self._context = context
        self._request = request
        self._dao = dao()  # construct DAO instance and inject

    # URLs are mapped to route names in __init__.py with Configurator.add_route()

    # For POST and PUT, we'll need to deserialize JSON to Person instances.
    # Pyramid's subproject Colander can do that, but the schema definition
    # is complex, so we'll just do it manually in the Person class.
    # For details of Colander, see
    # http://docs.pylonsproject.org/projects/colander/en/latest/

    # Pyramid calls this method for a request like this:
    # GET http://localhost:6543/rest/users/mike%@wxyz.com
    @view_config(request_method='GET',
                 route_name='rest_users_email',
                 renderer='json')
    def get_user_json(self):
        email = self._request.matchdict['email']
        return self.get_user(email)

    # FIXME: if this method is defined, requests without an Accept header
    # are always sent to it
    # @view_config(request_method='GET',
    #              route_name='rest_users_email',
    #              accept='application/xml')
    # def get_user_xml(self):
    #     email = self._request.matchdict['email']
    #     user = self.get_user(email)
    #     return UserServiceRest.user_to_xml(user)

    def get_user(self, email):
        """Fetch a Person by searching for the registered email address."""
        logger.debug("%s: email = %s", func_name(self), email)
        try:
            person = self._dao.get(email, self._request.db_session)
            logger.debug("%s: person = %s", func_name(self), 
                         str(vars(person)) if person else "null")
            if not person:
                raise HTTPNotFound()
        except PersistenceError:
            raise HTTPNotFound()
        return person

    @staticmethod
    def user_to_xml(user):  # FIXME: complete this method
        # create xml manually as in 10-41 and 10-42
        return '<user/>'

    @view_config(request_method='POST',
                 route_name='rest_users')
    def add_user(self):
        """Add a new Person."""
        # parse JSON in POST body
        json_body = self._request.json_body
        logger.debug("%s: request body = %s", func_name(self), json_body)
        new_user = Person()
        new_user.from_json(json_body)
        try:
            self._dao.add(new_user, self._request.db_session)
            return Response(
                status_int=201,
                content_type='application/json; charset=UTF-8')
        except Exception:
            msg = "Could not add user {}".format(new_user)
            logger.exception(msg)
            raise HTTPInternalServerError(msg)

    @view_config(request_method='PUT',
                 route_name='rest_users')
    def update_user(self):
        """Update an existing Person."""
        # parse JSON in PUT body
        json_body = self._request.json_body
        logger.debug("%s: request body = %s", func_name(self), json_body)
        new_user = Person()
        new_user.from_json(json_body)
        try:
            self._dao.update(new_user, self._request.db_session)
        except Exception:
            logger.exception("Problem updating Person {}".format(new_user))
            raise HTTPNotFound()
        return Response(status_int=202)

    @view_config(request_method='DELETE',
                 route_name='rest_users_email')
    def delete_user(self):
        """Delete a Person by searching for the registered email address."""
        email = self._request.matchdict['email']
        logger.debug("%s: email = %s", func_name(self), email)
        try:
            self._dao.delete(email, self._request.db_session)
        except PersistenceError:
            raise HTTPNotFound()
        return Response(status_int=204)
