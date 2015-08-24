"""
news_type.py - Defines an enum type NewsTypes.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from enum import Enum, unique


@unique
class NewsType(Enum):
    music = 0,
    sports = 1,
    theater = 2,
    movies = 3
