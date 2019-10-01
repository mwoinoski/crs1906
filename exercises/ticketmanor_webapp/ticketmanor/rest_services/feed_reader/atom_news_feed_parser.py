"""
AtomNewsFeedParser is an Atom news feed parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

from datetime import datetime
from time import strptime
from xml.dom import minidom
import re

from ticketmanor.util.utils import html_unescape
from ticketmanor.rest_services.feed_reader.news_feed_parser import (
    NewsFeedParser,
)


class AtomNewsFeedParser(NewsFeedParser):
    """Parses an AtomPub news feed"""
    feed_type = 'atom'
    item_element = 'entry'

    def __init__(self):
        super().__init__(AtomNewsFeedParser.item_element)

    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news/headlines?output={}&pz=1&ned=us&hl=en&' \
               'q={}'.format(AtomNewsFeedParser.feed_type, news_type)

    # def parse_xml_content(self, raw_content, max_items=0):
    #     """Implementation of abstract method"""
    #     parsed_content = []
    #     dom = minidom.parseString(raw_content)
    #
    #     for i, node in enumerate(dom.getElementsByTagName('entry'), start=1):
    #         parsed_item = self.parse_item(node)
    #         parsed_content.append(parsed_item)
    #         if i >= max_items > 0:
    #             break
    #
    #     return parsed_content

    def parse_item(self, node):
        """Implementation of abstract method defined in NewsFeedParser"""
        parsed_item = {}
        try:
            parsed_item['title'] = \
                node.getElementsByTagName('title')[0] \
                    .childNodes[0].nodeValue
        except IndexError:
            parsed_item['title'] = ''
        parsed_item['content'] = ''
        parsed_item['image_banner'] = ''
        parsed_item['image_thumbnail'] = ''
        try:
            desc_raw = \
                node.getElementsByTagName('content')[0] \
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
                node.getElementsByTagName('link')[0].getAttribute('href')
        except IndexError:
            parsed_item['link'] = ''
        try:
            updated = \
                node.getElementsByTagName('updated')[0] \
                    .childNodes[0].nodeValue
            # 2015-06-02T22:11:58Z
            parsed_item['date_time'] = \
                datetime(*strptime(updated, '%Y-%m-%dT%H:%M:%SZ')[0:6]) \
                    .strftime('%a, %d %b %Y %H:%M:%S GMT')
        except IndexError:
            parsed_item['date_time'] = ''

        return parsed_item
