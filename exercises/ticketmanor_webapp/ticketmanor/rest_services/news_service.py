"""
Pyramid View Callable for requests related to reading news feeds.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from pyramid.view import view_config
import logging
from .feed_reader.feed_reader import FeedReader
from ..util.utils import func_name

logger = logging.getLogger(__name__)


class NewsServiceView:
    """View Callable for reading news feeds"""

    def __init__(self, request):
        self._request = request
        self._news_reader = FeedReader()

    # URLs map to route names in __init__.py with Configurator.add_route()

    # Pyramid calls this method for a request like this:
    # GET http://localhost:6543/rest/events/{news_type}/news/news.json?max_items=3
    @view_config(request_method="GET",
                 route_name='get_news',
                 renderer='json')
    def get_news(self):
        news_type = self._request.matchdict['news_type']
        max_items = int(self._request.params.get('max_items', '0'))
        logger.debug("%s: news_type = %s, max_items = %s",
                     func_name(self), news_type, max_items)

        news_items = self._news_reader.get_news(news_type, max_items)

        for id, news_item in enumerate(news_items):
            news_item['id'] = id

        return news_items

    # Pyramid calls this method for a request like this:
    # GET http://localhost:6543/rest/events/{news_type}/news/{item_id}.json
    @view_config(request_method="GET",
                 route_name='get_news_item',
                 renderer='json')
    def get_news_item(self):
        news_type = self._request.matchdict['news_type']
        item_id = self._request.matchdict['item_id']
        logger.debug("%s: news_type = %s, item_id = %s",
                     func_name(self), news_type, item_id)

        news_items = self._news_reader.get_news(news_type)

        id = int(item_id)
        return news_items[id if id < len(news_items) else 0]
