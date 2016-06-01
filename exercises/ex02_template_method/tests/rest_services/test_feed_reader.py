"""
Unit tests for FeedReader class.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest.mock import Mock
from itertools import zip_longest
from unittest import TestCase, main
from ticketmanor.rest_services.feed_reader.feed_reader import FeedReader


class TestFeedReader(TestCase):
    """Unit tests for FeedReader"""

    def setUp(self):
        # The arg to FeedReader.__init__() is the class of the news feed
        # parser. FeedReader will call the constructor of the news feed parser
        # class, so we'll let it create a Mock, then we can access the Mock as
        # an attribute of the feed parser.
        self.feed_reader = FeedReader(news_feed_parser_class=Mock)

    def test_get_news_music(self):
        # The Mock will create new mocks anytime an attribute is referenced.
        # In the following statement, mocks are created for the
        # _news_feed_parser and get_news attributes. Because get_news is a
        # method, we can also set the method's return value.
        self.feed_reader._news_feed_parser.get_news.return_value = expected

        # The feed reader's get_news() method delegates to the news feed
        # parser's get_news(), which is a mock that we created in the previous
        # statement. The parser's get_news() will return the value of the
        # "expected" list.
        news = self.feed_reader.get_news("music")

        for expected_result, actual_result in zip_longest(expected, news):
            self.assertEqual(expected_result, actual_result)

    def test_get_news_max_items_1(self):
        self.feed_reader._news_feed_parser.get_news.return_value = expected[:1]

        news = self.feed_reader.get_news("music", max_items=1)

        for expected_result, actual_result in zip_longest(expected[:1], news):
            self.assertEqual(expected_result, actual_result)

    def test_get_news_max_items_2(self):
        self.feed_reader._news_feed_parser.get_news.return_value = expected[:2]

        news = self.feed_reader.get_news("music", max_items=2)

        for expected_result, actual_result in zip_longest(expected[:2], news):
            self.assertEqual(expected_result, actual_result)

expected = [
    {
        "title": "The Othello of Soul Music - Wall Street Journal",
        "date_time": "Fri, 29 May 2015 18:14:00 GMT",
        "image_thumbnail": "https://t0.gstatic.com/images?q=tbn:...",
        "image_banner": "https://t0.gstatic.com/images?q=tbn:...",
        "content": "Otis Redding is the Othello of soul music..."
    },
    {
        "title": "Second Item",
        "date_time": "Fri, 29 May 2015 19:25:00 GMT",
        "image_thumbnail": "https://t0.gstatic.com/images?q=tbn:...",
        "image_banner": "https://t0.gstatic.com/images?q=tbn:...",
        "content": "Second item content..."
    },
    {
        "title": "Third Item",
        "date_time": "Fri, 29 May 2015 20:36:00 GMT",
        "image_thumbnail": "https://t0.gstatic.com/images?q=tbn:...",
        "image_banner": "https://t0.gstatic.com/images?q=tbn:...",
        "content": "Third item content..."
    },
]

if __name__ == '__main__':
    main()
