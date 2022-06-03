"""
RssNewsFeedParser is an RSS news feed parser classes.

Adapted from examples in "Learning Python Design Patterns Code"
by Gennadiy Zlobin.

Converted to Python 3 by running:
    python PYTHON_HOME/Tools/Scripts/2to3.py -w news_parser.py
"""

import re
import urllib.request

from ticketmanor.util.utils import html_unescape
from ticketmanor.rest_services.feed_reader.news_feed_parser import (
    NewsFeedParser,
)
from ticketmanor.rest_services.feed_reader.rss_dummy_news import RssDummyNews


# TODO: make RssNewsFeedParser a subclass of NewsFeedParser
class RssNewsFeedParser(NewsFeedParser):
    """Parses a RSS news feed"""
    feed_type = 'rss'  # class attribute

    def __init__(self):
        self.item_element_name = 'item'
        # TODO: call the superclass __init__() method. Pass the value
        #       of the item_element_name data attribute as an argument.
        super().__init__(self.item_element_name)

    # TODO: cut the get_news() method out of this class and paste it
    #       into the NewsFeedParser class.

    # TODO: note that get_url() is a subclass hook method that will be
    #       called by the superclass template method.
    #       (no code changes required)
    def get_url(self, news_type):
        """Implementation of abstract method"""
        return 'https://news.google.com/news/headlines?output={}&pz=1&ned=us&hl=en&q={}'\
            .format(RssNewsFeedParser.feed_type, news_type)

    # TODO: cut the get_raw_content() method out of this class and paste it
    #       into the NewsFeedParser class.

    # TODO: note that get_dummy_news() is a subclass hook method that will be
    #       called by the superclass template method.
    #       (no code changes required)
    def get_dummy_news(self, url, news_type):
        """Called if the URL can't be opened"""
        return RssDummyNews.get_news(news_type)

    # TODO: cut the parse_xml_content() method out of this class and paste it
    #       into the NewsFeedParser class.

    # TODO: note that parse_item() is a subclass hook method that will be
    #       called by the superclass template method.
    #       (no code changes required)
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
