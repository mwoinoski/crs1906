"""
Unit tests for RssNewsFeedParser class.
"""

import unittest
from unittest import TestCase, skip
from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)
from ticketmanor.rest_services.feed_reader import FeedReaderException

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

# TODO: note the value of the `xml_input` variable. This is a simulated XML RSS
# news feed that will be used as input when testing RssNewsFeedParser methods.
# (no code changes required)

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
# of parsing the RSS XML news feed in the `xml_input` variable. You'll
# reference `expected` in your test cases.
# (no code changes required)

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


# TODO: make TestRssNewsFeedParser a subclass of unittest.TestCase
# HINT: see slide 3-8
class TestRssNewsFeedParser:
    """Unit tests for RssNewsFeedParser"""

    # TODO: Define a test method named test_get_news_music
    ....
        # TODO: in the test_get_news_music method, create an instance of
        # RssNewsFeedParser and save a reference to it in a local variable
        ....

        # TODO:
        # 1. call the news feed parser's get_news() method, passing 'music' as
        #    the argument
        # 2. save the list returned by the method in a local variable
        #    named `actual`
        ....

        # TODO: call a method that asserts the list named `expected` is
        # equal to the list named `actual`, which was returned from get_news()
        # HINT: see slide 3-11
        ....

    # TODO: Define a test method named test_get_news_music_max_items_1
    ....
        # TODO: in the test_get_news_music_max_items_1 method, create an
        # instance of RssNewsFeedParser and save a reference to it in a
        # local variable.
        ....

        # TODO:
        # 1. call the feed reader's get_news() method, passing
        #    news_type='music' and max_items=1 as the arguments.
        # 2. save the list returned by the method in a local variable
        ....

        # TODO: assert that the returned list has length 1 and that the first
        # item of the `expected` list equals the first item of the returned 
        # list.
        # HINT: use the built-in function len(), or use list slicing
        ....


    # TODO: Define a test method named test_get_news_invalid_news_type
    ....

        # TODO: in the test_get_news_invalid_news_type method, create an
        # instance of RssNewsFeedParser and save a reference to it in a
        # local variable.
        ....

        # TODO: Call an assert method to verify that if you call the
        # feed reader's get_news() method with an invalid news type argument
        # (for example, 'pluto'), the method raises a FeedReaderException.
        # HINT: see slide 3-15
        ....


    # TODO: examine the remaining test cases and be sure you understand
    # how they work.
    # (no code changes required)

    def test_get_news_music_zip_longest(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.get_news('music')

        self.assertEqual(expected, actual)

    def test_get_news_max_items_1(self):
        feed_reader = RssNewsFeedParser()

        # Note the call FeedReader.get_news() with a max_items argument
        actual = feed_reader.get_news('music', max_items=1)

        # Note the use of list slicing in the following assertion to verify
        # that the actual returned list contains only one item.
        self.assertEqual(expected[:1], actual)

    def test_get_news_max_items_2(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.get_news('music', max_items=2)

        self.assertEqual(expected[:2], actual)

    def test_parse_content(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input)

        self.assertEqual(expected, actual)

    def test_parse_content_max_items_1(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=1)

        self.assertEqual(expected[:1], actual)

    def test_parse_content_max_items_2(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=2)

        self.assertEqual(expected[:2], actual)

    @classmethod
    def setUpClass(cls):
        """
        Monkey patch RssNewsFeedParser.get_raw_content.

        We discuss monkey patching in the second section of the Unit Testing
        chapter.
        """
        RssNewsFeedParser.get_raw_content = lambda self, url, ntype: xml_input


if __name__ == '__main__':
    # TODO: call unittest.main()
    ....
