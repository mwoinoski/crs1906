__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from enum import Enum, unique


class FeedReaderException(Exception):
    """Exception class for all errors related to FeedReader"""
    pass


@unique
class NewsType(Enum):
    """Valid news types for news feeds"""
    music = 0,
    sports = 1,
    theater = 2,
    movies = 3
