"""
NewsFeedParser is an abstract base class for concrete news parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""  # noqa

from abc import ABC, abstractmethod
from typing import List, Dict
import urllib.request
import urllib.error
from xml.dom.minidom import Element
from xml.dom import minidom
from ticketmanor.rest_services.feed_reader import (
    NewsType,
    FeedReaderException,
)


class NewsFeedParser(ABC):
    """NewsFeedParser fetches the content of a news feed.

    Concrete subclasses may access news from different feed types, for
    example, an RSS feed or an Atom feed.

    NewsFeedParser is implemented with the Template Method GoF design pattern.
    """

    def __init__(self, news_item_element_name: str) -> None:
        self.item_element_name: str = news_item_element_name

    # TODO: you will write unit tests for the get_news() method. Examine the
    #       get_news() method below and be sure you understand how it works.
    #       (no code changes required)
    def get_news(self, news_type: str, max_items: int = 0) -> List[Dict[str, str]]:
        """A Template method. Returns latest news for a news website."""

        if news_type not in NewsType.__members__:
            raise FeedReaderException(
                '"{}" is not a recognized news type'.format(news_type))

        url: str = self.get_url(news_type)

        raw_content: bytes = self.get_raw_content(url, news_type)

        # TODO: note that the parse_xml_content() method returns a list of
        #       dictionaries, where each dictionary contains the data from a single
        #       news item.
        #       (no code changes required).
        content: List[Dict[str, str]] = self.parse_xml_content(raw_content, max_items)

        # TODO: note that get_news() returns the list of news items.
        #       (no code changes required).
        return content

    @abstractmethod
    def get_url(self, news_type: str) -> str:
        """
        Subclass hook method to get the URL of a news feed that the subclass
        can parse.
        """

    # This method could be static here in the base class, but we'll leave it
    # defined as an instance method so subclasses can override it if needed.
    def get_raw_content(self, url: str, news_type: str = None) -> bytes:
        # if url is not accessible, return dummy content
        try:
            return urllib.request.urlopen(url, timeout=5).read()
        except urllib.error.URLError:
            return self.get_dummy_news(url, news_type)

    def parse_xml_content(self, raw_content: bytes, max_items: int = 0) -> List[Dict[str, str]]:
        """
        Parses the raw content from an XML news feed into a list of news items.

        :param raw_content: byte string of well-formed XML
        :param max_items: maximum number of news items to return
        :return: list of news items. Each news item is a dictionary with keys
        title, link, content, date_time, image_banner, and image_thumbnail
        """
        parsed_content: List[Dict[str, str]] = []

        dom = minidom.parseString(raw_content.decode())

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
    def parse_item(self, node: Element) -> Dict[str, str]:
        """
        Subclass hook method.
        The ELement parameter represents the XML of a news items from the
        news feed. The XML elements are specific to each news feed type.
        This method converts the ELement to a dict with generic keys
        so that all news feed types can be processed in the same way.
        The keys in the returned dict are:
            title
            link
            content
            image_banner
            image_thumbnail
            image_banner
            date_time
        """

    def get_dummy_news(self, url: str, news_type: str) -> bytes:
        """
        Subclass can override this method to provide dummy news when the
        news feed URL is not reachable.
        """
        raise urllib.error.URLError("can't open connection to " + url)
