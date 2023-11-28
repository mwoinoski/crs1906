"""
Unit tests for RssNewsFeedParser class.
"""

import re
import pytest
from pytest import raises

from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)
from ticketmanor.rest_services.feed_reader import FeedReaderException

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

# TODO: note the value of the `xml_input` variable. This is a simulated XML RSS
#       news feed that will be used as input when testing RssNewsFeedParser methods.
#       (no code changes required)

xml_input = \
    '<rss>' \
        '<item>' \
            '<title>The Othello of Soul Music - Wall Street Journal</title>' \
            '<link>http://news.google.com/news/url/1</link>' \
            '<pubDate>Fri, 29 May 2015 18:14:00 GMT</pubDate>' \
            '<description>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:..."&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Otis Redding is the Othello of soul &lt;b&gt;music&lt;/b&gt;' \
                '...&lt;/font&gt;' \
            '</description>' \
        '</item>' \
        '<item>' \
            '<title>Second Item</title>' \
            '<link>http://news.google.com/news/url/2</link>' \
            '<pubDate>Fri, 29 May 2015 19:25:00 GMT</pubDate>' \
            '<description>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:..."&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Second item content...&lt;/font&gt;' \
            '</description>' \
        '</item>' \
        '<item>' \
            '<title>Third Item</title>' \
            '<link>http://news.google.com/news/url/3</link>' \
            '<pubDate>Fri, 29 May 2015 20:36:00 GMT</pubDate>' \
            '<description>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:..."&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Third item content...&lt;/font&gt;' \
            '</description>' \
        '</item>' \
    '</rss>'

# TODO: note the value of the `expected` variable. This is the expected result
#       of parsing the RSS XML news feed in the `xml_input` variable. You'll
#       reference `expected` in your test cases.
#       (no code changes required)

expected = [
    {
        'title': 'The Othello of Soul Music - Wall Street Journal',
        'link': 'http://news.google.com/news/url/1',
        'date_time': 'Fri, 29 May 2015 18:14:00 GMT',
        'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
        'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
        'content': 'Otis Redding is the Othello of soul music...'
    },
    {
        'title': 'Second Item',
        'link': 'http://news.google.com/news/url/2',
        'date_time': 'Fri, 29 May 2015 19:25:00 GMT',
        'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
        'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
        'content': 'Second item content...'
    },
    {
        'title': 'Third Item',
        'link': 'http://news.google.com/news/url/3',
        'date_time': 'Fri, 29 May 2015 20:36:00 GMT',
        'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
        'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
        'content': 'Third item content...'
    },
]


class TestRssNewsFeedParser:
    """Unit tests for RssNewsFeedParser"""

    # TODO: Define a test method named test_get_news_music
    def test_get_news_music(self):
        # TODO: in the test_get_news_music method, create an instance of
        #       RssNewsFeedParser and save a reference to it in a local variable
        feed_reader = RssNewsFeedParser()

        # Note that our goal is to test NewsFeedParser.get_news. But we
        # can't call the constructor for NewsFeedParser because it's an
        # abstract class, so instead we call the constructor for its
        # subclass RssNewsFeedParser

        # TODO: 1. call the news feed parser's get_news() method, passing 'music' as
        #          the argument
        #       2. save the list returned by the method in a local variable
        #          named `actual`
        actual = feed_reader.get_news('music')

        # TODO: assert that the list named `expected` is equal to the list named
        #       `actual`, which was returned from get_news()
        assert expected == actual

    # TODO: Define a test method named test_get_news_music_max_items_1
    def test_get_news_music_max_items_1(self):
        # TODO: in the test_get_news_music_max_items_1 method, create an
        #       instance of RssNewsFeedParser and save a reference to it in a
        #       local variable.
        feed_reader = RssNewsFeedParser()

        # TODO: 1. call the feed reader's get_news() method, passing
        #          news_type='music' and max_items=1 as the arguments.
        #       2. save the list returned by the method in a local variable
        actual = feed_reader.get_news('music', max_items=1)

        # TODO: assert that the returned list has length 1 and that the first
        #       item of the `expected` list equals the first item of the returned 
        #       list.
        assert 1 == len(actual)
        assert expected[0] == actual[0]

        # Note that you can combine the two previous assertions into one using
        # list slicing:
        assert expected[:1] == actual
        # Because both arguments to assert are lists, the method
        # compares the lists' lengths and their contents.

    # TODO: Define a test method named test_get_news_invalid_news_type
    def test_get_news_invalid_news_type(self):
        # TODO: in the test_get_news_invalid_news_type method, create an
        #       instance of RssNewsFeedParser and save a reference to it in a
        #       local variable.
        feed_reader = RssNewsFeedParser()

        # TODO: add a `with` statement to assert that if you call the
        #       feed reader's get_news() method with an invalid news type argument
        #       (for example, 'pluto'), the method raises a FeedReaderException.
        with raises(FeedReaderException):
            feed_reader.get_news('pluto')

    # TODO: examine the remaining test cases and be sure you understand
    #       how they work.
    #       (no code changes required)

    def test_get_news_max_items_2(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.get_news('music', max_items=2)

        assert expected[:2] == actual

    def test_parse_content(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input)

        assert expected == actual

    def test_parse_content_max_items_1(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=1)

        assert expected[:1] == actual

    def test_parse_content_max_items_2(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=2)

        assert expected[:2] == actual

    def test_get_dummy_news(self):
        feed_reader = RssNewsFeedParser()

        dummy_news = feed_reader.get_dummy_news('', 'movies')

        assert re.match(r'^\s*<rss.*</rss>\s*$', dummy_news, flags=re.DOTALL)

    def test_parse_content_items_missing(self):
        feed_reader = RssNewsFeedParser()

        minimal_input = '<rss><item></item></rss>'
        minimal_results = [
            {
                'title': '',
                'link': '',
                'date_time': '',
                'image_thumbnail': '',
                'image_banner': '',
                'content': ''
            }
        ]

        actual_results = feed_reader.parse_xml_content(minimal_input)

        assert minimal_results == actual_results


@pytest.fixture(autouse=True, scope='function')
def parser_monkey_patch():
    """
    Monkey patch RssNewsFeedParser.get_raw_content to return our mock XML input.
    (We discuss monkey patching in the second section of the Unit Testing
    chapter.)
    """
    RssNewsFeedParser.get_raw_content = lambda self, url, ntype: xml_input
