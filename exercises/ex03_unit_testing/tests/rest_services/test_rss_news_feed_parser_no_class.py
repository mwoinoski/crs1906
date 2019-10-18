"""
Unit tests for RssNewsFeedParser class defined with no TestCase subclass.
"""

from pytest import raises
from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)
from ticketmanor.rest_services.feed_reader import FeedReaderException

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


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

# TODO: note that there is no TestCase subclass defined in this module.
# The test cases are ordinary functions rather than methods.
# (no code changes required)

# TODO:
# 1. Copy the following methods from test_rss_news_feed_parser.py and
#    paste them here:
#       test_get_news_music()
#       test_get_news_music_max_items_1()
#    (Be sure to un-indent the function definitions)
# 2. Delete the "self" argument from the copied functions.
# 3. Replace calls to self.assertEqual() with the assert statement.
#    HINT: see slide 3-19
...


# TODO: copy the test_get_news_invalid_news_type() method from
# test_rss_news_feed_parser.py and paste it here. Modify it to use the
# pytest.raises() function to verify that a FeedReaderException is raised.
# HINT: see slide 3-22
...


def test_get_news_max_items_2():
    feed_reader = RssNewsFeedParser()

    actual = feed_reader.get_news('music', max_items=2)

    assert expected[:2] == actual


def test_parse_content():
    feed_reader = RssNewsFeedParser()

    actual = feed_reader.parse_xml_content(xml_input)

    assert expected == actual


def test_parse_content_max_items_1():
    feed_reader = RssNewsFeedParser()

    actual = feed_reader.parse_xml_content(xml_input, max_items=1)

    assert expected[:1] == actual


def test_parse_content_max_items_2():
    feed_reader = RssNewsFeedParser()

    actual = feed_reader.parse_xml_content(xml_input, max_items=2)

    assert expected[:2] == actual


def test_parse_content_items_missing():
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


# Monkey patch RssNewsFeedParser.get_raw_content.
# We will discuss monkey patching in the second section of the Unit Testing
# chapter.
RssNewsFeedParser.get_raw_content = lambda self, url, max_items: xml_input


# TODO: note that there is no call to unittest.main().
# (no code changes required)
