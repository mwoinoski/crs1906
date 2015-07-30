"""
RssNewsFeedParser is an RSS news feed parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

from xml.dom import minidom
import re

from ticketmanor.util.utils import html_unescape
from ticketmanor.rest_services.feed_reader.news_feed_parser import NewsFeedParser


class RssNewsFeedParser(NewsFeedParser):
    """Parses a RSS news feed"""
    feed_type = "rss"

    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news?output={}&pz=1&ned=us&hl=en&q={}' \
            .format(RssNewsFeedParser.feed_type, news_type)

    def parse_content(self, raw_content):
        """Implementation of abstract method"""
        parsed_content = []
        dom = minidom.parseString(raw_content)

        for node in dom.getElementsByTagName('item'):
            parsed_item = {}

            try:
                parsed_item['title'] = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = ""

            parsed_item['content'] = ""
            parsed_item['image_banner'] = ""
            parsed_item['image_thumbnail'] = ""
            try:
                desc_raw = node.getElementsByTagName('description')[0].childNodes[0].nodeValue
                desc_html = html_unescape(desc_raw)
                match = re.match(r'.*?<img src="([^"]*).*', desc_html)
                if match:
                    parsed_item['image_thumbnail'] = match.group(1)
                    parsed_item['image_banner'] = match.group(1)
                match = re.match(r'.*?<div class="lh">.*?<br>.*?<br>.*?<font[^>]*>(.*?)</font>.*', desc_html)
                if match:
                    parsed_item['content'] = re.sub(r'</?b>', '', match.group(1))
            except IndexError:
                pass

            try:
                parsed_item['link'] = node.getElementsByTagName('link')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['link'] = ""

            try:
                parsed_item['date_time'] = node.getElementsByTagName('pubDate')[0].childNodes[0].nodeValue
                # Tue, 02 Jun 2015 11:25:05 GMT
            except IndexError:
                parsed_item['date_time'] = ""

            parsed_content.append(parsed_item)

        return parsed_content
