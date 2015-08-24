"""
Unit tests for AtomNewsFeedParser class.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from itertools import zip_longest
from ticketmanor.rest_services.feed_reader.atom_news_feed_parser import (
    AtomNewsFeedParser,
)


class TestAtomNewsFeedParser(TestCase):
    """Unit tests for AtomNewsFeedParser"""

    def test_get_news_music(self):
        feed_reader = AtomNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input)

        for expected_result, actual_result in zip_longest(expected, actual):
            self.assertEquals(expected_result, actual_result)

    def test_get_news_max_items_1(self):
        feed_reader = AtomNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=1)

        for expected_result, actual_result in zip_longest(expected[:1], actual):
            self.assertEquals(expected_result, actual_result)

    def test_get_news_max_items_2(self):
        feed_reader = AtomNewsFeedParser()

        actual = feed_reader.parse_xml_content(xml_input, max_items=2)

        for expected_result, actual_result in zip_longest(expected[:2], actual):
            self.assertEquals(expected_result, actual_result)

xml_input = \
    '<feed>' \
        '<entry>' \
            '<title>The Othello of Soul Music - Wall Street Journal</title>' \
            '<updated>2015-08-19T07:00:08Z</updated>' \
            '<link type="text/html" href="http://news.google.com/news/url/1"></link>' \
            '<content>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:..."&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Otis Redding is the Othello of soul &lt;b&gt;music&lt;/b&gt;' \
                '...&lt;/font&gt;' \
            '</content>' \
        '</entry>' \
        '<entry>' \
            '<title>Second Item</title>' \
            '<updated>2015-08-19T08:00:08Z</updated>' \
            '<link type="text/html" href="http://news.google.com/news/url/2"></link>' \
            '<content>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:..."&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Second item content...&lt;/font&gt;' \
            '</content>' \
        '</entry>' \
        '<entry>' \
            '<title>Third Item</title>' \
            '<updated>2015-08-19T09:00:08Z</updated>' \
            '<link type="text/html" href="http://news.google.com/news/url/3"></link>' \
            '<content>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:..."&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Third item content...&lt;/font&gt;' \
            '</content>' \
        '</entry>' \
    '</feed>'

expected = [
    {'title': 'The Othello of Soul Music - Wall Street Journal',
     'date_time': 'Wed, 19 Aug 2015 07:00:08 GMT',
     'link': 'http://news.google.com/news/url/1',
     'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
     'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
     'content': 'Otis Redding is the Othello of soul music...'},
    {'title': 'Second Item',
     'date_time': 'Wed, 19 Aug 2015 08:00:08 GMT',
     'link': 'http://news.google.com/news/url/2',
     'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
     'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
     'content': 'Second item content...'},
    {'title': 'Third Item',
     'date_time': 'Wed, 19 Aug 2015 09:00:08 GMT',
     'link': 'http://news.google.com/news/url/3',
     'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
     'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
     'content': 'Third item content...'},
]

if __name__ == '__main__':
    main()
