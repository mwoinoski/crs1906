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
# TODO: you'll be testing the UserServiceRest class.
# (no code change required)
class UserServiceRest:
    """View Callable for managing users with REST web service requests."""

    # TODO: note the UserServiceRest __init__() method takes a DAO class as an
    # argument.
    # (no code change required)
    def __init__(self, context, request, dao=PersonDao):
        """DAO dependency will be injected from dao arg"""
        self._context = context
        self._request = request

        # TODO: note how the _dao attribute is set by calling a DAO
        # constructor. This results in a hard-coded dependency between the
        # UserServiceRest class and the DAO class.
        # (no code change required)
        self._dao = dao()  # construct DAO instance and inject

    @view_config(request_method='GET',
                 route_name='rest_users_email',
                 renderer='json')
    # TODO: you will be testing this get_user() method.
    # (no code change required)
    def get_user(self):
        email = self._request.matchdict['email']
        return self.get_user_by_email(email)

    @view_config(request_method='GET', route_name='rest_users_email')
    def get_user_by_email(self, email):
        """Fetch a Person by searching for the registered email address."""
        logger.debug("%s: email = %s", func_name(self), email)

        # TODO: note the call to the DAO's get() method.
        # (no code change required)
        try:
            person = self._dao.get(email, self._request.db_session)

        # TODO: note that if the DAO's get() method raises a PersistenceError,
        # we'll raise an HTTPNotFound exception.
        # (no code change required)
        except PersistenceError:
            raise HTTPNotFound()

        logger.debug("%s: person = %s", func_name(self), str(vars(person)))
        return person

    @view_config(request_method='POST', route_name='rest_users')
    # TODO: you will be testing this add_user() method.
    # (no code change required)
    def add_user(self):
        """Add a new Person."""
        # parse JSON in POST body
        json_body = self._request.json_body
        logger.debug("%s: request body = %s", func_name(self), json_body)
        new_user = Person()
        new_user.from_json(json_body)

        # TODO: note the call the DAO's add() method
        # (no code change required)
        try:
            self._dao.add(new_user, self._request.db_session)
            return Response(
                status_int=201,
                content_type='application/json; charset=UTF-8')

        # TODO: note that if the DAO's add() method raises an Exception,
        # we'll raise an HTTPInternalServerError.
        # (no code change required)
        except Exception:
            msg = "Could not add user {}".format(new_user)
            logger.exception(msg)
            raise HTTPInternalServerError(msg)

    @view_config(request_method='PUT', route_name='rest_users')
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

    @view_config(request_method='DELETE', route_name='rest_users_email')
    def delete_user(self):
        """Delete a Person by searching for the registered email address."""
        email = self._request.matchdict['email']
        logger.debug("%s: email = %s", func_name(self), email)
        try:
            self._dao.delete(email, self._request.db_session)
        except PersistenceError:
            raise HTTPNotFound()
        return Response(status_int=204)
