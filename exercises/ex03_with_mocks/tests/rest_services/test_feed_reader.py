"""
Unit tests for FeedReader class.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest.mock import Mock, patch
from unittest import TestCase, main, skip
from itertools import zip_longest
from ticketmanor.rest_services.feed_reader.feed_reader import FeedReader
from ticketmanor.rest_services.feed_reader import FeedReaderException
from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)


class TestFeedReader(TestCase):
    """Unit tests for FeedReader"""

    # This test method creates a Mock news feed parser
    def test_fetch_news_items_music(self):
        # TODO: create a Mock news feed parser object and assign it to a local
        # variable named `mock_news_feed_parser`
        # HINT: see slide 3-40
        mock_news_feed_parser = ...

        # TODO: assign the return value of the mock's get_news() method to a
        # local variable named `expected` 
        ...

        # TODO: create a FeedReader instance and assign it to a local variable
        # named `feed_reader`
        feed_reader = ...

        # TODO: set the feed_reader.news_feed_parser attribute to
        # mock_news_feed_parser
        ...

        # TODO: note the call the call to feed_reader.fetch_news_items().
        # Because you changed the feed reader's `news_feed_parser` attribute in
        # the previous statement, the feed_reader will get news from the mock
        # object instead of a RssNewsFeedParser instance.
        # (no code change required)
        news = feed_reader.fetch_news_items("music")

        # TODO: note that we verify the result as usual.
        # (no code change required)
        for expected_result, actual_result in zip_longest(expected, news):
            self.assertEqual(expected_result, actual_result)

    # This test method uses a Mock news feed parser to raise an exception
    def test_fetch_news_items_raise_FeedReaderException(self):
        # TODO: create a Mock news feed parser object and assign it to a local
        # variable named `mock_news_feed_parser`
        mock_news_feed_parser = ...

        # TODO: create a new Mock and assign it to the mock feed parser's
        # `get_news` attribute. The new Mock should have a side effect of
        # raising a FeedReaderException.
        # HINT: see slide 3-42
        ...

        # TODO: create a FeedReader instance and assign it to a local variable
        # named `feed_reader`
        feed_reader = ...

        # TODO: set the feed_reader.news_feed_parser attribute to
        # mock_news_feed_parser
        ...

        # TODO: call the feed_reader's fetch_news_items() method and save the
        # return value in a variable named `news`. (Pass any string as the
        # argument to fetch_news_items())
        news = ...

        # TODO: assert that the `news` variable is an instance of list.
        # HINT: use the built-in isinstance() function
        ...

        # TODO: assert that the length of the `news` list is 0
        ...

        # TODO: note that the call to fetch_news_items() will log a stack
        # trace, but as long as you get a green bar, the test case passed.
        # (no code change required)

    # TODO: use @patch.object to create a Mock. @patch.object will take
    # two arguments:
    # 1. the class to be mocked (RssNewsFeedParser)
    # 2. the name of the method to be mocked, as a string ('get_news')
    # HINT: see slide 3-43
    ...
    # TODO: note the second argument to the method, which will receive the Mock
    # object for the mocked method.
    # (no code change required)
    def test_get_news_with_patch(self, mock_get_news_method):
        # TODO: set the return value of the mocked method to the `expected`
	# variable (defined later)
        ...

        # TODO: note the call to the FeedReader constructor. The call to the
        # RssNewsFeedParser will happen as usual, but because we added
        # @patch.object to this test method, the RssNewsFeedParser's get_news
        # attribute will be replaced by a Mock.
        feed_reader = FeedReader()

        # TODO: note that the call to the feed_reader's fetch_news_items()
        # will call the Mock's get_news(), which you programmed to return
        # `expected`
        # (no code change required)
        news = feed_reader.fetch_news_items("music")

        for expected_result, actual_result in zip_longest(expected, news):
            self.assertEqual(expected_result, actual_result)

    # TODO: note the use of @patch to completely replace the RssNewsFeedParser
    # class. This ensures that its constructor is never called.
    # (no code change required)
    @patch('ticketmanor.rest_services.feed_reader.feed_reader.RssNewsFeedParser')
    def test_fetch_news_items_max_items_2(self, mock_news_feed_parser_class):
        # Always patch an object where it is imported, not where it is defined.
        # Here, we're testing a method in
        # ticketmanor.rest_services.feed_reader.feed_reader.FeedReader, which
        # imports RssNewsFeedParser. So to mock RssNewsFeedParser, patch()
        # needs to know the package that is importing RssNewsFeedParser, not
        # the package that defines RssNewsFeedParser.

        # TODO: note that the second argument to the test method is a
        # Mock class, not a Mock instance, so we need an additional step
        # to get a Mock instance for setting the get_news() return value.
        # (no code change required)
        mock_news_feed_parser = mock_news_feed_parser_class.return_value
        mock_news_feed_parser.get_news.return_value = expected

        feed_reader = FeedReader()
        # TODO: Add a print() statement to RssNewsFeedParser.__init__() to
        # verify that the constructor is never called.

        news = feed_reader.fetch_news_items("music", 2)

        # TODO: verify the mock_news_feed_parser.get_news method was called
        # arguments "music" and 2
        # HINT: see slide 3-41
        ...

        for expected_result, actual_result in zip_longest(expected, news):
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
