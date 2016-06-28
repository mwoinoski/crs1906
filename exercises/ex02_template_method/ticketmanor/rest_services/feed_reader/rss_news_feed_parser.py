"""
RssNewsFeedParser is an RSS news feed parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

import re
import urllib.request
from xml.dom import minidom

from ticketmanor.util.utils import html_unescape
from ticketmanor.rest_services.feed_reader.news_feed_parser import (
    NewsFeedParser,
    NewsType,
    FeedReaderException,
)
from ticketmanor.rest_services.feed_reader.rss_dummy_news import RssDummyNews


# TODO: make RssNewsFeedParser a subclass of NewsFeedParser
class RssNewsFeedParser:
    """Parses a RSS news feed"""
    feed_type = 'rss'

    def __init__(self):
        self.item_element_name = 'item'
        # TODO: call the superclass __init__() method. Pass the value
        # of the item_element_name data attribute as an argument.
        ....

    # TODO: cut the get_news() method out of this class and paste it
    # into the NewsFeedParser class.
    # HINT: Be sure to delete get_news() from this file after pasting
    # it into news_feed_parser.py.
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
        raw_content = self.get_raw_content(url, news_type)

        # TODO: note the call to the generic superclass method
        # parse_xml_content() to convert the raw XML content to Python data.
        # (no code changes required)
        content = self.parse_xml_content(raw_content, max_items)

        return content

    # TODO: note that get_url() is a subclass hook method that will be
    # called by the superclass template method.
    # (no code changes required)
    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news?output={}&pz=1&ned=us&hl=en&q={}'\
            .format(RssNewsFeedParser.feed_type, news_type)

    # TODO: cut the get_raw_content() method out of this class and paste it
    # into the NewsFeedParser class.
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

    # TODO: note that get_dummy_news() is a subclass hook method that will be
    # called by the superclass template method.
    # (no code changes required)
    def get_dummy_news(self, url, news_type):
        """Called if the URL can't be opened"""
        return RssDummyNews.get_news(news_type)

    # TODO: cut the parse_xml_content() method out of this class and paste it
    # into the NewsFeedParser class.
    def parse_xml_content(self, raw_content, max_items=0):
        # TODO: note that parse_xml_content() is a generic superclass method
        # that will be called by the superclass template method.

        dom = minidom.parseString(raw_content)

        # BONUS TODO 2: convert this method into a generator function that
        # yields a single parsed item each time it's called.
        # HINT: delete the parse_content list completely. Instead of appending
        # each parsed item to a list, yield it from the generator.

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
            parsed_item = ....

            # TODO: append parsed_item to parsed_content
            ....

            if i >= max_items > 0:
                break

        # TODO: note that the method returns `parsed_content`
        # (no code change required)
        return parsed_content
        # Return value is a list of news items. Each news item is a dictionary
        # with keys title, link, content, date_time, image_banner, and
        # image_thumbnail

    # TODO: note that parse_item() is a subclass hook method that will be
    # called by the superclass template method.
    # (no code changes required)
    def parse_item(self, item_node):
        """Implementation of a method called from NewsFeedParser"""
        parsed_item = {}
        try:
            title_node = item_node.getElementsByTagName('title')[0]
            parsed_item['title'] = title_node.childNodes[0].nodeValue
        except IndexError:
            parsed_item['title'] = ''
        try:
            link_node = item_node.getElementsByTagName('link')[0]
            parsed_item['link'] = link_node.childNodes[0].nodeValue
        except IndexError:
            parsed_item['link'] = ''
        try:
            parsed_item['content'] = ''
            parsed_item['image_banner'] = ''
            parsed_item['image_thumbnail'] = ''
            description_node = item_node.getElementsByTagName('description')[0]
            desc_raw = description_node.childNodes[0].nodeValue
            desc_html = html_unescape(desc_raw)
            match = re.match(r'.*?<img src="([^"]*).*', desc_html)
            if match:
                parsed_item['image_thumbnail'] = match.group(1)
                parsed_item['image_banner'] = match.group(1)
            match = re.match(r'.*?<div class="lh">.*?<br>.*?<br>.*?'
                             r'<font[^>]*>(.*?)</font>.*', desc_html)
            if match:
                parsed_item['content'] = re.sub(r'</?b>', '', match.group(1))
        except IndexError:
            pass
        try:
            pub_date_node = item_node.getElementsByTagName('pubDate')[0]
            parsed_item['date_time'] = pub_date_node.childNodes[0].nodeValue
            # date_time: Tue, 02 Jun 2015 11:25:05 GMT
        except IndexError:
            parsed_item['date_time'] = ''
        return parsed_item
