"""
Convenience constants for card library modules.
"""


class Rank:
    """ Constants for rank of a playing card. """
    ACE = 1
    JACK = 11
    QUEEN = 12
    KING = 13
    chars = " A23456789TJQK"

    def get_rank_chars(self) -> str:
        """ Return the rank character string. """
        return self.chars


class Suit:
    """ Constants for the suit of a playing card. """
    CLUBS = 0
    CLUB_SYMBOL = "♣"       # '\u2663'
    DIAMONDS = 1
    DIAMOND_SYMBOL = '♦'    # '\u2666'
    HEARTS = 2
    HEART_SYMBOL = '♥'      # \u2665'
    SPADES = 3
    SPADE_SYMBOL = '♠'      # \u2660'
    chars = CLUB_SYMBOL+DIAMOND_SYMBOL+HEART_SYMBOL+SPADE_SYMBOL

    def get_suit_chars(self) -> str:
        """ Return the suit character string. """
        return self.chars
