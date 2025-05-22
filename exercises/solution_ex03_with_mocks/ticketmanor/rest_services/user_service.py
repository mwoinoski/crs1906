"""
Pyramid View Callable for requests related to user management.
"""
from pyramid.response import Response
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'  # noqa


from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError
import logging
from ..util.utils import func_name
from ..models.person import Person

logger = logging.getLogger(__name__)


@view_defaults(renderer='json')
class UserServiceRest:
    """View Callable for managing users"""

    def __init__(self, context, request, dao):
        """DAO dependency will be injected from dao arg"""
        if isinstance(dao, type):  # the param is a reference to a DAO class
            dao = dao()  # construct an instance of the given class

        # TODO: note that this class has a dependency on a DAO
        self._dao = dao

        self._context = context
        self._request = request

    # TODO: this is the method you will test
    def get_user(self, email):
        """Fetch a Person by searching for the registered email address."""
        try:
            # TODO: note the call to the DAO's `get` method to look up a person
            #       in the database
            person = self._dao.get(email, self._request.db_session)

            # TODO: note that if the person is not in the database,
            #       this method raises an HTTPNotFound exception
            if not person:
                raise HTTPNotFound()

        # TODO: note that if the DAO's `get` method raises an exception,
        #       this method raises an HTTPNotFound exception
        except PersistenceError:
            raise HTTPNotFound()

        return person

    @view_config(request_method='GET',
                 route_name='rest_users_email',
                 renderer='json')
    def get_user_json(self):
        email = self._request.matchdict['email']
        return self.get_user(email)

    @staticmethod
    def user_to_xml(user):  # noqa
        # create stub xml manually
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
            self._request.db_session.commit()
            return Response(
                status_int=201,
                content_type='application/json; charset=UTF-8')
        except Exception:
            msg = "Could not add user {}".format(new_user)
            logger.exception(msg)
            self._request.db_session.rollback()
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
            self._request.db_session.commit()
        except Exception:
            logger.exception("Problem updating Person {}".format(new_user))
            self._request.db_session.rollback()
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
            self._request.db_session.commit()
        except PersistenceError:
            logger.exception(f"Problem deleting Person {email}")
            self._request.db_session.rollback()
            raise HTTPNotFound()
        return Response(status_int=204)
