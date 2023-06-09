"""
Unit tests for FeedReader class.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest.mock import Mock, patch
from itertools import zip_longest
from ticketmanor.rest_services.feed_reader.feed_reader import FeedReader
from ticketmanor.rest_services.feed_reader import FeedReaderException
from ticketmanor.rest_services.feed_reader.rss_news_feed_parser import (
    RssNewsFeedParser,
)


class TestFeedReader:
    """Unit tests for FeedReader"""

    # This test method creates a Mock news feed parser
    def test_fetch_news_items_music(self):
        # TODO: create a mock RssNewsFeedParser object and assign it to a local
        #       variable named `mock_news_feed_parser`
        # HINT: see slide 3-39
        mock_news_feed_parser = ....

        # TODO: set the return value of the mock's get_news() method to the
        #       value of the variable `expected` (defined at the end of the file)
        ....

        # TODO: create a FeedReader instance and assign it to a local variable
        #       named `feed_reader`
        feed_reader = ....

        # TODO: set the feed_reader.news_feed_parser attribute to the
        #       mock_news_feed_parser
        ....

        # TODO: note the call the call to feed_reader.fetch_news_items().
        #       Because you changed the feed reader's `news_feed_parser` attribute in
        #       the previous statement, the feed_reader will get news from the mock
        #       object instead of a RssNewsFeedParser instance.
        #       (no code change required)
        news = feed_reader.fetch_news_items("music")

        # TODO: note that we verify the result as usual.
        #       (no code change required)
        for expected_result, actual_result in zip_longest(expected, news):
            assert expected_result == actual_result

    # TODO: After you get the first test case running, uncomment the following
    #       test case and make the required changes. Then run the file again and
    #       verify this second test case passes.

    # # This test method uses a Mock news feed parser to raise an exception
    # def test_fetch_news_items_raise_feedreaderexception(self):
    #     # TODO: create a mock RssNewsFeedParser object and assign it to a local
    #     #       variable named `mock_news_feed_parser`
    #     mock_news_feed_parser = ....
    #
    #     # TODO: set the `side_effect` attribute of the mock's `get_news` method
    #     #       so it raises a FeedReaderException when called.
    #     # HINT: see slide 3-38
    #     ....
    #
    #     # TODO: create a FeedReader instance and assign it to a local variable
    #     #       named `feed_reader`
    #     feed_reader = ....
    #
    #     # TODO: set the feed_reader.news_feed_parser attribute to
    #     #       mock_news_feed_parser
    #     ....
    #
    #     # TODO: call the feed_reader's fetch_news_items() method and save the
    #     #       return value in a variable named `news`. (Pass any string as the
    #     #       argument to fetch_news_items())
    #     news = ....
    #
    #     # TODO: assert that the `news` variable is an instance of list.
    #     # HINT: use the built-in isinstance() function
    #     ....
    #
    #     # TODO: assert that the length of the `news` list is 0
    #     ....
    #
    #     # TODO: note that the call to fetch_news_items() will log a stack
    #     #       trace, but as long as you get a green bar, the test case passed.
    #     #       (no code change required)


    # TODO: examine the remaining test cases and be sure you understand
    #       how they work.
    #       (no code changes required)

    def test_fetch_news_items_max_items_1(self):
        # test set up
        mock_news_feed_parser = Mock(spec=RssNewsFeedParser)
        mock_news_feed_parser.get_news.return_value = expected
        feed_reader = FeedReader()
        feed_reader.news_feed_parser = mock_news_feed_parser

        # call method under test
        news = feed_reader.fetch_news_items("music", 1)

        # verify that the mock's get_news() method was called correctly
        # (for details, see Appendix B)
        mock_news_feed_parser.get_news.assert_called_once_with("music", 1)
        # verify results
        for expected_result, actual_result in zip_longest(expected, news):
            assert expected_result == actual_result

    def test_fetch_news_items_max_items_2(self):
        # test set up
        mock_news_feed_parser = Mock(spec=RssNewsFeedParser)
        mock_news_feed_parser.get_news.return_value = expected
        feed_reader = FeedReader()
        feed_reader.news_feed_parser = mock_news_feed_parser

        # call method under test
        news = feed_reader.fetch_news_items("music", 2)

        # verify that the mock's get_news() method was called correctly
        # (for details, see Appendix B)
        mock_news_feed_parser.get_news.assert_called_once_with("music", 2)
        # verify results
        for expected_result, actual_result in zip_longest(expected, news):
            assert expected_result == actual_result

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
