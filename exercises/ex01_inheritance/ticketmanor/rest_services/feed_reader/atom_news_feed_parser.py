"""
AtomNewsFeedParser is an Atom news feed parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

from datetime import datetime
from time import strftime, strptime
from xml.dom import minidom
import re

from ticketmanor.util.utils import html_unescape
from ticketmanor.rest_services.feed_reader.news_feed_parser import NewsFeedParser


class AtomNewsFeedParser(NewsFeedParser):
    """Parses a AtomPub news feed"""
    feed_type = "atom"

    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news?output={}&pz=1&ned=us&hl=en&q={}' \
            .format(AtomNewsFeedParser.feed_type, news_type)

    def parse_content(self, raw_content):
        """Implementation of abstract method"""
        parsed_content = []
        dom = minidom.parseString(raw_content)

        for node in dom.getElementsByTagName('entry'):

            parsed_item = {}

            try:
                parsed_item['title'] = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = ""

            parsed_item['content'] = ""
            parsed_item['image_banner'] = ""
            parsed_item['image_thumbnail'] = ""
            try:
                desc_raw = node.getElementsByTagName('content')[0].childNodes[0].nodeValue
                desc_html = html_unescape(desc_raw)
                match = re.match(r'.*?<img src="([^"]*).*', desc_html)
                if match:
                    parsed_item['image_thumbnail'] = match.group(1)
                    parsed_item['image_banner'] = match.group(1)
                match = re.match(r'.*?<div class="lh">.*?<br>.*?<br>.*?<font[^>]*>(.*?)</font>.*', desc_html)
                if match:
                    parsed_item['content'] = match.group(1)
            except IndexError:
                pass

            try:
                parsed_item['link'] = node.getElementsByTagName('link')[0].getAttribute('href')
            except IndexError:
                parsed_item['link'] = ""

            try:
                updated = node.getElementsByTagName('updated')[0].childNodes[0].nodeValue
                # 2015-06-02T22:11:58Z
                parsed_item['date_time'] = \
                    datetime(*strptime(updated, "%Y-%m-%dT%H:%M:%SZ")[0:6]) \
                        .strftime("%a, %d %b %Y %H:%M:%S GMT")
            except IndexError:
                parsed_item['date_time'] = ""

            parsed_content.append(parsed_item)

        return parsed_content
