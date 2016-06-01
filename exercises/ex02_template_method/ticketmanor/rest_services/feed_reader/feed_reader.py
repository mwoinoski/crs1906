"""
FeedReader class reads various feeds (for example, RSS and AtomPub).
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from .rss_news_feed_parser import (
    RssNewsFeedParser,
)


class FeedReader:
    """Base class for all FeedReader types"""

    def __init__(self, news_feed_parser_class=RssNewsFeedParser):
        """
        Initialize the FeedReader.

        :param news_feed_parser_class the class of a parser for the news feed.
        The FeedReader instance will call the constructor of the parser class.
        This is a simple implementation of dependency injection, which allows
        the dependency to be satisfied dynamically.
        """
        self._news_feed_parser = news_feed_parser_class()  # call constructor

    def get_news(self, news_type, max_items=0):
        """
        Get news items of type news_type.

        If max_items > 0, return no more than max_items news items.
        Otherwise, returns all news items
        """

        return self._news_feed_parser.get_news(news_type, max_items)
