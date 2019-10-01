"""
FeedReader class reads various feeds (for example, RSS, AtomPub).
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import logging
from .rss_news_feed_parser import RssNewsFeedParser
from . import FeedReaderException

logger = logging.getLogger(__name__)


# TODO: FeedReader is the class you will be testing.
# (no code change required)
class FeedReader:
    """Base class for all FeedReader types"""

    def __init__(self, news_feed_parser=RssNewsFeedParser):
        """Initialize the FeedReader."""
        # TODO: note that the parameter `news_feed_parser` is the class of a 
        # parser for the news feed. The FeedReader instance will call the 
        # constructor of the parser class. This is a simple implementation of 
        # dependency injection, which allows the dependency to be satisfied 
        # dynamically. Unit tests will pass a mock news feed parser class as 
        # the `news_feed_parser` parameter, while production code will allow 
        # the parameter to default to the production parser class.
        # (no code change required)

        self._news_feed_parser = news_feed_parser()


    def fetch_news_items(self, news_type, max_items=0):
        """
        Get news items of type news_type.

        If max_items > 0, return no more than max_items news items.
        Otherwise, returns all news items
        """

        # TODO: note the call to the feed parser's get_news() method.
        # (no code change required)
        try:
            return self.news_feed_parser.get_news(news_type, max_items)

        # TODO: note that if the call to get_news() raises an exception,
        # this method returns an empty list.
        # (no code change required)
        except FeedReaderException as e:
            logger.exception('Problem getting {} news with {} max items'
                             .format(news_type, max_items))
            return []
