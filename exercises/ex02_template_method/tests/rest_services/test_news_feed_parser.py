"""
Unit tests for NewsFeedParser class.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from ticketmanor.rest_services.feed_reader.news_feed_parser import (
    NewsFeedParser,
)


class TestNewsFeedParser(TestCase):
    """Unit tests for NewsFeedParser"""

    def test_class_is_abstract(self):
        # if a class is abstract, a constructor call will raise TypeError
        with self.assertRaises(TypeError, msg='NewsFeedParser is not abstract'):
            NewsFeedParser(None)


if __name__ == '__main__':
    main()
