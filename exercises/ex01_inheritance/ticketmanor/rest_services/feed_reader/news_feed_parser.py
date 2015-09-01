"""
NewsFeedParser is an abstract base class for concrete news parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

from abc import ABCMeta, abstractmethod
import urllib.request
from xml.dom import minidom
from ticketmanor.rest_services.feed_reader import (
    NewsType,
    FeedReaderException,
)


class NewsFeedParser(metaclass=ABCMeta):
    """NewsFeedParser fetches the content of a news feed.

    Concrete subclasses may access news from different feed types, for
    example, an RSS feed or an Atom feed.

    NewsFeedParser is implemented with the Template Method GoF design pattern.
    """

    def __init__(self, news_item_element_name):
        self.item_element_name = news_item_element_name

    def get_news(self, news_type, max_items=0):
        """A Template method. Returns latest news for a news website."""

        if news_type not in NewsType.__members__:
            raise FeedReaderException(
                '"{}" is not a recognized news type'.format(news_type))

        url = self.get_url(news_type)

        raw_content = self.get_raw_content(url)

        content = self.parse_xml_content(raw_content, max_items)

        return content

    @abstractmethod
    def get_url(self, news_type):
        pass

    # This method could be static here in the base class, but we'll leave it
    # defined as an instance method so subclasses can override it if needed.
    # noinspection PyMethodMayBeStatic
    def get_raw_content(self, url):
        return urllib.request.urlopen(url).read()

    def parse_xml_content(self, raw_content, max_items=0):
        """
        Parses a raw content string from an XML news feed into a list of
        news items.

        :param raw_content: string of well-formed XML
        :param max_items: maximum number of news items to return
        :return: list of news items. Each news item is a dictionary with keys
        title, link, content, date_time, image_banner, and image_thumbnail
        """
        parsed_content = []
        dom = minidom.parseString(raw_content)

        for i, node in enumerate(
                dom.getElementsByTagName(self.item_element_name), start=1):
            # Call the subclass's override of the abstract method parse_item()
            parsed_content.append(self.parse_item(node))
            # We create the list here and slice it later, but we want to avoid
            # creating a huge list if we need only a few items.
            if i >= max_items > 0:
                break

        return parsed_content

    @abstractmethod
    def parse_item(self, node):
        pass
