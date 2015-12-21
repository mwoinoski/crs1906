"""
NewsFeedParser is an abstract base class for concrete news parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_feed_parser.py
"""

from abc import ABCMeta, abstractmethod
import urllib.request
from xml.dom import minidom
from ticketmanor.rest_services.feed_reader import (
    NewsType,
    FeedReaderException,
)


# BONUS TODO: make NewsFeedParser an abstract base class
class NewsFeedParser(metaclass=ABCMeta):

    # TODO: note the definition of the NewsFeedParser __init__() method.
    # (no code changes required)
    def __init__(self, news_item_element_name):
        self.item_element_name = news_item_element_name

    # TODO: paste methods from rss_news_feed_parser here

    def get_news(self, news_type, max_items=0):
        # TODO: note that get_news() is the superclass template method.
        # It is called by NewsServiceView.get_news() in news_service.py
        # (no code changes required)

        if news_type not in NewsType.__members__:
            raise FeedReaderException(
                '"{}" is not a recognized news type'.format(news_type))

        # TODO: note the call to the subclass hook method get_url(), which
        # returns the URL of the news feed.
        # (no code changes required)
        url = self.get_url(news_type)

        # TODO: note the call to the generic superclass method
        # get_raw_content() to get the raw XML content from the URL.
        # (no code changes required)
        raw_content = self.get_raw_content(url)

        # TODO: note the call to the generic superclass method
        # parse_xml_content() to convert the raw XML content to Python data.
        # (no code changes required)
        content = self.parse_xml_content(raw_content, max_items)

        return content

    def get_raw_content(self, url, news_type=None):
        # TODO: note that get_raw_content() is a generic superclass method that
        # will be called by the superclass template method.
        try:
            return urllib.request.urlopen(url, timeout=1).read()
        except urllib.request.URLError:
            # TODO: note the call to the subclass hook method get_dummy_news(),
            # which returns dummy content if the URL is not accessible.
            # (no code changes required)
            return self.get_dummy_news(url, news_type)

    def parse_xml_content(self, raw_content, max_items=0):
        # TODO: note that parse_xml_content() is a generic superclass method
        # that will be called by the superclass template method.

        dom = minidom.parseString(raw_content)

        # TODO: note the definition of the list named `parsed_content`.
        # (no code change required)
        parsed_content = []

        # TODO: note the assignment of `item_node` on the `for` loop below.
        # (no code change required)
        for i, item_node in enumerate(
                dom.getElementsByTagName(self.item_element_name), start=1):

            # TODO: call the subclass hook method parse_item(),
            # passing item_node as the parameter.
            # Save the return value of parse_item() in a local variable
            # named `parsed_item`.
            parsed_item = self.parse_item(item_node)

            # TODO: append parsed_item to parsed_content
            parsed_content.append(parsed_item)

            if i >= max_items > 0:
                break

        # TODO: note that the method returns `parsed_content`
        # (no code change required)
        return parsed_content
        # Return value is a list of news items. Each news item is a dictionary
        # with keys title, link, content, date_time, image_banner, and
        # image_thumbnail

    # BONUS TODO 2: convert parse_xml_content() into a generator function that
    # yields a single parsed item each time it's called.
    # HINT: delete the parse_content list completely. Instead of appending
    # each parsed item to a list, yield it from the generator.
    # def parse_xml_content(self, raw_content, max_items=0):
    #     dom = minidom.parseString(raw_content)
    #     for i, item_node in enumerate(
    #             dom.getElementsByTagName(self.item_element_name), start=1):
    #         # Get the parsed news item
    #         parsed_item = self.parse_item(item_node)
    #         # Yield each item from the generator function
    #         yield parsed_item
    #
    #         if i >= max_items > 0:
    #             break
    #     # At this point, there's nothing else to return
    #     return

    # BONUS TODO: define get_url() as an abstract method
    @abstractmethod
    def get_url(self, news_type):
        pass

    # BONUS TODO: define parse_item() as an abstract method
    @abstractmethod
    def parse_item(self, item_node):
        pass

    # BONUS TODO: define get_dummy_news() as an abstract method
    def get_dummy_news(self, url, news_type):
        pass

# Run news_feed_parser to verify NewsFeedParser is abstract
if __name__ == '__main__':
    try:
        parser = NewsFeedParser(None)
        import sys
        print("\nERROR: NewsFeedParser is not abstract", file=sys.stderr)
    except TypeError:
        print("\nSuccess: NewsFeedParser is abstract")
