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


# BONUS TODO: make NewsFeedParser an abstract base class
class NewsFeedParser(metaclass=ABCMeta):

    # TODO: note the definition of the NewsFeedParser __init__() method.
    # (no code changes required)
    def __init__(self, news_item_element_name):
        self.item_element_name = news_item_element_name

    # TODO: paste methods from rss_news_feed_parser here

    def get_news(self, news_type, max_items=0):
        """Return latest news for a news website."""

        # TODO: note the call to the subclass's override of
        # the get_url() method to get the URL of the news feed.
        # (no code changes required)
        url = self.get_url(news_type)

        # TODO: note the call to a base class method to get the raw XML content
        # from the URL.
        # (no code changes required)
        raw_content = self.get_raw_content(url)

        # TODO: note the call to the base class parse_xml_content() method
        # to parse the raw XML.
        # (no code changes required)
        content = self.parse_xml_content(raw_content, max_items)

        return content

    # BONUS TODO: define get_url() as an abstract method
    @abstractmethod
    def get_url(self, news_type):
        pass

    def get_raw_content(self, url):
        """Get the XML content at the given URL"""
        return urllib.request.urlopen(url).read()

    def parse_xml_content(self, raw_content, max_items=0):
        """
        Parses a raw content string from an XML news feed into a tree of
        DOM nodes.

        :param raw_content: string of well-formed XML
        :param max_items: maximum number of news items to return
        :return: list of news items. Each news item is a dictionary with
        keys title, link, content, date_time, image_banner, and image_thumbnail
        """
        dom = minidom.parseString(raw_content)

        # BONUS TODO 2: convert this method into a generator function that yields
        # a single parsed item each time it's called.
        # HINT: delete the parse_content list completely. Instead of appending
        # each parsed item to a list, yield it from the generator.

        for i, item_node in enumerate(
                dom.getElementsByTagName(self.item_element_name), start=1):

            # TODO: call the subclass's override of the parse_item() method
            # and save the return value in a new variable
            parsed_item = self.parse_item(item_node)

            # TODO: append the item returned by the call to parse_item() to
            # the list name parsed_content
            yield parsed_item

            if i >= max_items > 0:
                break

        return

    # BONUS TODO: define parse_item() as an abstract method
    @abstractmethod
    def parse_item(self, item_node):
        pass
