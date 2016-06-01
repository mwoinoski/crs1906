"""
Unit tests for RssNewsFeedParser class.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main, skip
from itertools import zip_longest
from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)
from ticketmanor.rest_services.feed_reader import FeedReaderException


class TestRssNewsFeedParser(TestCase):
    """Unit tests for RssNewsFeedParser"""

    @classmethod
    def setUpClass(cls):
        """
        Monkey patch RssNewsFeedParser.get_raw_content.

        We discuss monkey patching in the second section of the Unit Testing
        chapter.
        """
        RssNewsFeedParser.get_raw_content = lambda self, url, ntype: xml_input

    def test_parse_content(self):
        feed_parser = RssNewsFeedParser()

        actual = feed_parser.parse_xml_content(xml_input)

        # By using itertools.zip_longest(), assertEquals() will eventually fail
        # if the lists are not the same length
        for expected_result, actual_result in zip_longest(expected, actual):
            self.assertEquals(expected_result, actual_result)

    def test_parse_content_max_items_1(self):
        feed_parser = RssNewsFeedParser()

        actual = feed_parser.parse_xml_content(xml_input, max_items=1)

        for expected_result, actual_result in zip_longest(expected[:1], actual):
            self.assertEquals(expected_result, actual_result)

    def test_parse_content_max_items_2(self):
        feed_parser = RssNewsFeedParser()

        actual = feed_parser.parse_xml_content(xml_input, max_items=2)

        for expected_result, actual_result in zip_longest(expected[:2], actual):
            self.assertEquals(expected_result, actual_result)

    def test_parse_content_items_missing(self):
        feed_parser = RssNewsFeedParser()

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

        actual_results = feed_parser.parse_xml_content(minimal_input)

        self.assertEquals(minimal_results, actual_results)

    def test_get_news_music(self):
        feed_parser = RssNewsFeedParser()

        actual = feed_parser.get_news('music')

        for expected_result, actual_result in zip_longest(expected, actual):
            self.assertEquals(expected_result, actual_result)

    def test_get_news_max_items_1(self):
        feed_parser = RssNewsFeedParser()

        actual = feed_parser.get_news('music', max_items=1)

        for expected_result, actual_result in zip_longest(expected[:1], actual):
            self.assertEquals(expected_result, actual_result)

    def test_get_news_max_items_2(self):
        feed_parser = RssNewsFeedParser()

        actual = feed_parser.get_news('music', max_items=2)

        for expected_result, actual_result in zip_longest(expected[:2], actual):
            self.assertEquals(expected_result, actual_result)

    def test_get_news_invalid_news_type(self):
        feed_parser = RssNewsFeedParser()
        with self.assertRaises(FeedReaderException):
            feed_parser.get_news('pluto')


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

if __name__ == '__main__':
    main()
