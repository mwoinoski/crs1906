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
)


# TODO: make RssNewsFeedParser a subclass of NewsFeedParser
class RssNewsFeedParser(NewsFeedParser):
    """Parses a RSS news feed"""
    feed_type = 'rss'

    def __init__(self):
        self.item_element_name = 'item'
        # TODO: call the superclass's __init__() method. Pass the value
        # of the item_element_name data attribute as an argument.
        super().__init__(self.item_element_name)

    # TODO: cut the get_news() method out of this class and paste it
    # into the NewsFeedParser class.
    # HINT: Be sure to delete get_news() from this file after pasting
    # it into news_feed_parser.py.
    # def get_news(self, news_type, max_items=0):
    #     """Return latest news for a news website."""
    #
    #     # TODO: note the call to the subclass's override of
    #     # the get_url() method to get the URL of the news feed.
    #     # (no code changes required)
    #     url = self.get_url(news_type)
    #
    #     # TODO: note the call to a base class method to get the raw XML content
    #     # from the URL.
    #     # (no code changes required)
    #     raw_content = self.get_raw_content(url)
    #
    #     # TODO: note the call to the base class parse_xml_content() method
    #     # to parse the raw XML.
    #     # (no code changes required)
    #     content = self.parse_xml_content(raw_content, max_items)
    #
    #     return content

    # TODO: note that the get_url() method will be called by the
    # base class's template method.
    # (no code changes required)
    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news?output={}&pz=1&ned=us&hl=en&q={}'\
            .format(RssNewsFeedParser.feed_type, news_type)

    # TODO: cut the get_raw_content() method out of this class and paste it
    # into the NewsFeedParser class.
    # HINT: Be sure to delete get_raw_content() from this file after pasting
    # it into news_feed_parser.py.
    # def get_raw_content(self, url):
    #     """Get the XML content at the given URL"""
    #     return urllib.request.urlopen(url).read()

    # TODO: cut the parse_xml_content() method out of this class and paste it
    # into the NewsFeedParser class.
    # HINT: Be sure to delete parse_xml_content() from this file after pasting
    # it into news_feed_parser.py.
    # def parse_xml_content(self, raw_content, max_items=0):
    #     """
    #     Parses a raw content string from an XML news feed into a tree of
    #     DOM nodes.
    #
    #     :param raw_content: string of well-formed XML
    #     :param max_items: maximum number of news items to return
    #     :return: list of news items. Each news item is a dictionary with
    #     keys title, link, content, date_time, image_banner, and image_thumbnail
    #     """
    #     parsed_content = []
    #     dom = minidom.parseString(raw_content)
    #
    #     for i, item_node in enumerate(
    #             dom.getElementsByTagName(self.item_element_name), start=1):
    #
    #         # TODO: call the subclass's override of the parse_item() method
    #         # and save the return value in a new variable
    #         parsed_item = self.parse_item(item_node)
    #
    #         # TODO: append the item returned by the call to parse_item() to
    #         # the list name parsed_content
    #         parsed_content.append(parsed_item)
    #
    #         if i >= max_items > 0:
    #             break
    #
    #     return parsed_content

    # TODO: note that the parse_item() method will be called by the
    # base class's template method.
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
