"""
Unit tests for FeedReader class.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from unittest import TestCase, main
from ticketmanor.rest_services.feed_reader.feed_reader import FeedReader


# BONUS TODO: replace with Mock
class StubNewsFeedParser:
    def get_news(self, news_type, max_items=0):
        if max_items > 0:
            return expected_results[:max_items]
        return expected_results


class TestFeedReader(TestCase):
    """Unit tests for FeedReader"""

    def test_get_news_music(self):
        feed_reader = FeedReader(StubNewsFeedParser)

        actual_results = feed_reader.get_news("music")

        for i, actual_result in enumerate(actual_results, start=0):
            for name in 'title', 'date_time', 'image_thumbnail', \
                        'image_banner', 'content':
                self.assertTrue(expected_results[i][name], actual_result[name])
        self.assertEqual(2, i)

    def test_get_news_max_items_1(self):
        feed_reader = FeedReader()

        result = feed_reader.get_news("movies", max_items=1)

        self.assertTrue(len(result) == 1)

    def test_get_news_max_items_2(self):
        feed_reader = FeedReader()

        result = feed_reader.get_news("movies", max_items=2)

        self.assertTrue(len(result) == 2)

expected_results = [
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
