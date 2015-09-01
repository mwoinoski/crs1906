"""
AtomNewsFeedParser is an Atom news feed parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

from datetime import datetime
from time import strptime
import urllib.request
from xml.dom import minidom
import re

from ticketmanor.util.utils import html_unescape
from ticketmanor.rest_services.feed_reader.news_feed_parser import (
    NewsFeedParser,
)


# TODO: make AtomNewsFeedParser a subclass of NewsFeedParser
class AtomNewsFeedParser:
    """Parses an AtomPub news feed"""
    feed_type = 'atom'

    def __init__(self):
        self.item_element_name = 'entry'
        # TODO: call the superclass's __init__() method. Pass the value
        # of the item_element_name data attribute as an argument.


    # TODO: delete the get_news() method from this class.
    def get_news(self, news_type, max_items=0):
        """Return latest news for a news website."""
        url = self.get_url(news_type)
        raw_content = self.get_raw_content(url)
        content = self.parse_xml_content(raw_content, max_items)
        return content

    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news?output={}&pz=1&ned=us&hl=en&' \
               'q={}'.format(AtomNewsFeedParser.feed_type, news_type)

    # TODO: delete the get_raw_content() method from this class.
    def get_raw_content(self, url):
        """Get the XML content at the given URL"""
        return urllib.request.urlopen(url).read()

    # TODO: delete the parse_xml_content() method from this class.
    def parse_xml_content(self, raw_content, max_items=0):
        """
        Parses a raw content string from an XML news feed into a tree of
        DOM nodes.
        """
        parsed_content = []
        dom = minidom.parseString(raw_content)

        for i, item_node in enumerate(
                dom.getElementsByTagName(self.item_element_name), start=1):
            parsed_item = self.parse_item(item_node)
            parsed_content.append(parsed_item)
            if i >= max_items > 0:
                break

        return parsed_content

    def parse_item(self, item_node):
        """Implementation of a method called from NewsFeedParser"""
        parsed_item = {}
        try:
            parsed_item['title'] = \
                item_node.getElementsByTagName('title')[0] \
                    .childNodes[0].nodeValue
        except IndexError:
            parsed_item['title'] = ''
        parsed_item['content'] = ''
        parsed_item['image_banner'] = ''
        parsed_item['image_thumbnail'] = ''
        try:
            desc_raw = \
                item_node.getElementsByTagName('content')[0] \
                    .childNodes[0].nodeValue
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
            parsed_item['link'] = \
                item_node.getElementsByTagName('link')[0].getAttribute('href')
        except IndexError:
            parsed_item['link'] = ''
        try:
            updated = \
                item_node.getElementsByTagName('updated')[0] \
                    .childNodes[0].nodeValue
            # 2015-06-02T22:11:58Z
            parsed_item['date_time'] = \
                datetime(*strptime(updated, '%Y-%m-%dT%H:%M:%SZ')[0:6]) \
                    .strftime('%a, %d %b %Y %H:%M:%S GMT')
        except IndexError:
            parsed_item['date_time'] = ''

        return parsed_item
