__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from enum import Enum


class FeedReaderException(Exception):
    """Exception class for all errors related to FeedReader"""
    pass


class NewsType(Enum):
    """Valid news types for news feeds"""
    concerts = 0,
    music = 0,  # duplicate value ok
    sports = 1,
    theater = 2,
    movies = 3
