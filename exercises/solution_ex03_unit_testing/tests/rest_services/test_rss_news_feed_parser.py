"""
Unit tests for RssNewsFeedParser class.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import unittest
from unittest import TestCase, skip
from itertools import zip_longest
from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)
from ticketmanor.rest_services.feed_reader.feed_reader_exception import (
    FeedReaderException,
)

# TODO: note the value of the xml_input variable. This is a simulated XML RSS
# news feed that will be used as input when testing AtomNewsFeedParser methods.
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

# TODO: note the value of the "expected" variable. This is the expected result
# of parsing the RSS XML news feed in the xml_input variable. You'll reference
# "expected" in your test cases.
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
class TestRssNewsFeedParser(TestCase):
    """Unit tests for RssNewsFeedParser"""

    # TODO: Define a test method named test_get_news_music
    def test_get_news_music(self):
        # TODO: in the test_get_news_music method, create an instance of
        # RssNewsFeedParser and save a reference to it in a local variable
        feed_reader = RssNewsFeedParser()

        # TODO:
        # 1. call the feed reader's get_news() method, passing 'music' as the
        #    argument
        # 2. save the list returned by the method in a local variable
        actual = feed_reader.get_news('music')

        # TODO: add a method call that asserts the length of the returned list
        # is equal to 3
        # HINT: see slide 3-10
        self.assertEqual(3, len(actual))

        # TODO: loop over the list returned by get_news(). For each item on
        # the list, call an assert method that verifies the item is equal to
        # the corresponding item on the list named "expected".
        for i in range(3):
            self.assertEqual(expected[i], actual[i])

    # TODO: Define a test method named test_get_news_music_max_items_1
    def test_get_news_music_max_items_1(self):
        # TODO: in the test_get_news_music_max_items_1 method, create an
        # instance of RssNewsFeedParser and save a reference to it in a
        # local variable.
        feed_reader = RssNewsFeedParser()

        # TODO:
        # 1. call the feed reader's get_news() method, passing
        #    news_type='music' and max_items=1 as the arguments.
        # 2. save the list returned by the method in a local variable
        actual = feed_reader.get_news('music', max_items=1)

        # TODO: verify that the returned list has length 1 and that the
        # returned news item is equal to the first item on the "expected" list.
        self.assertEqual(1, len(actual))
        self.assertEqual(expected[0], actual[0])

    # TODO: Define a test method named test_get_news_invalid_news_type
    def test_get_news_invalid_news_type(self):
        # TODO: in the test_get_news_invalid_news_type method, create an
        # instance of RssNewsFeedParser and save a reference to it in a
        # local variable.
        feed_reader = RssNewsFeedParser()

        # TODO: Call an assert method to verify that if you call the
        # feed reader's get_news() method with an invalid news type argument
        # (for example, 'pluto'), the method raises a FeedReaderException.
        # HINT: see slide 3-15
        with self.assertRaises(FeedReaderException):
            feed_reader.get_news('pluto')

    # TODO: examine the remaining test cases and be sure you understand
    # how they work.
    # (no code changes required)

    def test_get_news_music_zip_longest(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.get_news('music')

        # By using itertools.zip_longest(), assertEquals() will eventually fail
        # if the lists are not the same length
        for expected_result, actual_result in zip_longest(expected, actual):
            self.assertEqual(expected_result, actual_result)

    def test_get_news_max_items_1(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.get_news('music', max_items=1)

        for expected_result, actual_result in zip_longest(expected[:1], actual):
            self.assertEquals(expected_result, actual_result)

    def test_get_news_max_items_2(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.get_news('music', max_items=2)

        for expected_result, actual_result in zip_longest(expected[:2], actual):
            self.assertEquals(expected_result, actual_result)

    def test_parse_content(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input)

        for expected_result, actual_result in zip_longest(expected, actual):
            self.assertEquals(expected_result, actual_result)

    def test_parse_content_max_items_1(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=1)

        for expected_result, actual_result in zip_longest(expected[:1], actual):
            self.assertEquals(expected_result, actual_result)

    def test_parse_content_max_items_2(self):
        feed_reader = RssNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=2)

        for expected_result, actual_result in zip_longest(expected[:2], actual):
            self.assertEquals(expected_result, actual_result)

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

        self.assertEquals(minimal_results, actual_results)

    @classmethod
    def setUpClass(cls):
        """
        Monkey patch RssNewsFeedParser.get_raw_content.

        We discuss monkey patching in the second section of the Unit Testing
        chapter.
        """
        RssNewsFeedParser.get_raw_content = lambda self, url: xml_input


if __name__ == '__main__':
    # TODO: call unittest.main()
    unittest.main()