"""
Pyramid View Callable for requests related to event management.
"""
import json
from pyramid.response import Response
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import logging
import random
from urllib.parse import unquote

from pyramid.view import view_config, notfound_view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound
from ..util.utils import func_name, SimpleJsonEncoder
from ..models.persistence.act_dao import ActDao
from ..models.act import Act
from ..models.event import Event
from . import notfound

logger = logging.getLogger(__name__)


@view_defaults(renderer='json')
class EventServiceRest:
    """View Callable for managing events"""

    def __init__(self, context, request, dao=ActDao):
        """DAO dependency will be injected from dao arg"""
        self._context = context
        self._request = request
        self._dao = dao()  # construct DAO instance and inject

    # URLs are mapped to route names in __init__.py with Configurator.add_route()

    # For POST and PUT, we'll need to deserialize JSON to Event instances.
    # Pyramid's subproject Colander can do that, but the schema definition
    # is complex, so we'll just do it manually in the Act and Event classes.
    # For details of Colander, see
    # http://docs.pylonsproject.org/projects/colander/en/latest/

    # Pyramid calls this method for a request like this:
    # GET http://localhost:6543/rest/events/music.json?title=London+Symphony
    @view_config(request_method='GET',
                 route_name='rest_events')
    def get_acts(self):
        """Fetch Acts that match the given query parameters"""
        # args = event_type=Artist,words=berlin
        logger.debug("%s: args = %s", func_name(self),
                     ','.join(['{}={}'.format(k, v)
                               for k, v in self._request.params.items()]))
        query_params = {}

        # get type from URL path: music, sports, or movies
        act_type = self._request.matchdict['type']

        search_type = self._request.params['event_type']
        # search_type for music/concerts is Artist, Venue, Date, or City

        search_terms = self._request.params.get('words', None)
        if search_terms:
            search_terms = unquote(search_terms).replace('+', ' ')
            query_params['title'] = search_terms

        act = self._dao.query_for_act(
            self._request.db_session,
            act_type=act_type,
            search_type=search_type,
            **query_params)

        # To implement paging, we can't splice acts.events directly
        # because SQLAlchemy is still managing the Act and will delete rows
        # from the EVENT table if we remove the associated Events from the
        # Act's events list. So we'll get the Act's data as a dictionary
        # and manipulate that instead. Pyramid can serialize either the Act
        # or a dictionary that contains the Act's data attributes.
        if act:
            act = act.__json__()
        if act and 'page' in self._request.params \
                and 'page_size' in self._request.params \
                and 'events' in act:
            act['page'] = int(self._request.params['page'])
            act['page_size'] = int(self._request.params['page_size'])
            start = act['page'] * act['page_size']
            act['events'] = act['events'][start:start + act['page_size']]
            # breakpoint()

        logger.debug("%s: found %d events for %s",
                     func_name(self),
                     len(act['events']) if act and 'events' in act and act['events'] else 0,
                     search_terms)

        return act

    # FIXME: add get_event(self, event_id)

    # FIXME:
    # @view_config(request_method='POST',
    #              route_name='rest_events')
    # def add_event(self):
    #     """Add a new Event."""
    #     # parse JSON in POST body
    #     json_body = self._request.json_body
    #     logger.debug("%s: request body = %s", func_name(self), json_body)
    #     new_event = Event()
    #     new_event.from_json(json_body)
    #     self._dao.add(new_event, self._request.db_session)
    #     return Response(
    #         status_int=201,
    #         content_type='application/json; charset=UTF-8')

    # FIXME
    # @view_config(request_method='PUT',
    #              route_name='rest_events')
    # def update_event(self):
    #     """Update an existing Event."""
    #     # parse JSON in PUT body
    #     json_body = self._request.json_body
    #     logger.debug("%s: request body = %s", func_name(self), json_body)
    #     new_event = Event()
    #     new_event.from_json(json_body)
    #     try:
    #         self._dao.update(new_event, self._request.db_session)
    #     except Exception as e:
    #         logger.debug("Problem updating Event " + str(new_event), exc_info=True)
    #         raise HTTPNotFound()
    #     return Response(status_int=202)

    # FIXME
    # @view_config(request_method='DELETE',
    #              route_name='rest_events_id')
    # def delete_event(self):
    #     """Delete a Event by searching for the registered id address."""
    #     id = self._request.matchdict['id']
    #     logger.debug("%s: id = %s", func_name(self), id)
    #     try:
    #         self._dao.delete(id, self._request.db_session)
    #     except PersistenceError:
    #         raise HTTPNotFound()
    #     return Response(status_int=202)
