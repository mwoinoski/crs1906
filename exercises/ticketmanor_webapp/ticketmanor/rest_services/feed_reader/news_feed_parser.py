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
        """A Template method. Returns latest news for every news website."""
        # Call subclass method to get URL
        url = self.get_url(news_type)
        raw_content = self.get_raw_content(url)
        # Call subclass method to parse content
        content = self.parse_content(raw_content)
        cropped = self.crop(content, max_items)
        return cropped

    @abstractmethod
    def get_url(self, news_type):
        pass

    def get_raw_content(self, url):
        return urllib.request.urlopen(url).read()

    @abstractmethod
    def parse_content(self, content):
        pass

    def crop(self, parsed_content, max_items):
        content = parsed_content
        if max_items > 0:
            content = parsed_content[:max_items]
        return content
