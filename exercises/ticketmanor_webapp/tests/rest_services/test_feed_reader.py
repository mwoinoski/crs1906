"""
Unit tests for FeedReader class.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from unittest import TestCase
from ticketmanor.rest_services.feed_reader.feed_reader import FeedReader


class StubNewsFeedParser:  # TODO: replace with Mock
    news_items = [
        {"title": "The Othello of Soul Music - Wall Street Journal",
         "date_time": "Fri, 29 May 2015 18:14:00 GMT",
         "image_url": "https://t0.gstatic.com/images?q=tbn:...",
         "content": "Otis Redding is the Othello of soul music..."},
        {"title": "Second Item",
         "date_time": "Fri, 29 May 2015 19:25:00 GMT",
         "image_url": "https://t0.gstatic.com/images?q=tbn:...",
         "content": "Second item content..."},
        {"title": "Third Item",
         "date_time": "Fri, 29 May 2015 20:36:00 GMT",
         "image_url": "https://t0.gstatic.com/images?q=tbn:...",
         "content": "Third item content..."},
    ]

    def get_news(self, news_type, max_items=0):
        if max_items > 0:
            return StubNewsFeedParser.news_items[:max_items]
        return StubNewsFeedParser.news_items


class TestFeedReader(TestCase):
    """Unit tests for FeedReader"""

    def test_get_news_music(self):
        feed_reader = FeedReader(StubNewsFeedParser)

        result = feed_reader.get_news("music")

        self.assertEqual(3, len(result))
        for news_item in result:
            self.assertTrue(len(news_item['title']) > 0)
            self.assertTrue(len(news_item['date_time']) > 0)
            self.assertTrue(len(news_item['image_url']) > 0)
            self.assertTrue(len(news_item['content']) > 0)

    def test_get_news_max_items_1(self):
        feed_reader = FeedReader()

        result = feed_reader.get_news("movies", max_items=1)

        self.assertTrue(len(result) == 1)

    def test_get_news_max_items_2(self):
        feed_reader = FeedReader()

        result = feed_reader.get_news("movies", max_items=2)

        self.assertTrue(len(result) == 2)
