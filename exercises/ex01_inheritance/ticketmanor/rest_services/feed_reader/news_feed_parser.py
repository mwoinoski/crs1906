"""
NewsFeedParser is an abstract base class for concrete news parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""
from abc import ABCMeta, abstractmethod
import urllib.request


class NewsFeedParser(metaclass=ABCMeta):
    """NewsFeedParser fetches the content of a news feed.

    Concrete subclasses may access news from different feed types, for
    example, an RSS feed or an Atom feed.

    NewsFeedParser is implemented with the Template Method GoF design pattern.
    """

    def get_news(self, news_type, max_items=0):
        """A Template method. Returns latest news for a news website."""

        # Call subclass method to get the URL of the news feed
        url = self.get_url(news_type)

        # Call base class method to get the raw content from the URL
        raw_content = self.get_raw_content(url)

        # Call subclass method to parse content
        content = self.parse_content(raw_content, max_items)
        return content

    @abstractmethod
    def get_url(self, news_type):
        pass

    # This method could be static here in the base class, but we'll leave it
    # defined as an instance method so subclasses can override it if needed.
    # noinspection PyMethodMayBeStatic
    def get_raw_content(self, url):
        return urllib.request.urlopen(url).read()

    @abstractmethod
    def parse_content(self, content):
        pass
