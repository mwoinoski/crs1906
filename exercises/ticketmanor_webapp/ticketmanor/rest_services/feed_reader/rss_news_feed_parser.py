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
        return 'https://news.google.com/news?output={}&pz=1&ned=us&hl=en&q={}'\
            .format(RssNewsFeedParser.feed_type, news_type)

    def parse_content(self, raw_content, max_items=0):
        """Implementation of abstract method defined in NewsFeedParser"""
        parsed_content = []
        dom = minidom.parseString(raw_content)

        for count, node in enumerate(dom.getElementsByTagName('item'), start=1):
            parsed_item = RssNewsFeedParser._parse_item(node)
            parsed_content.append(parsed_item)
            if count >= max_items > 0:
                break

        return parsed_content

    @staticmethod
    def _parse_item(node):
        parsed_item = {}
        try:
            title_node = node.getElementsByTagName('title')[0]
            parsed_item['title'] = title_node.childNodes[0].nodeValue
        except IndexError:
            parsed_item['title'] = ""
        parsed_item['content'] = ""
        parsed_item['image_banner'] = ""
        parsed_item['image_thumbnail'] = ""
        try:
            description_node = node.getElementsByTagName('description')[0]
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
            link_node = node.getElementsByTagName('link')[0]
            parsed_item['link'] = link_node.childNodes[0].nodeValue
        except IndexError:
            parsed_item['link'] = ""
        try:
            pub_date_node = node.getElementsByTagName('pubDate')[0]
            parsed_item['date_time'] = pub_date_node.childNodes[0].nodeValue
            # date_time: Tue, 02 Jun 2015 11:25:05 GMT
        except IndexError:
            parsed_item['date_time'] = ""
        return parsed_item
