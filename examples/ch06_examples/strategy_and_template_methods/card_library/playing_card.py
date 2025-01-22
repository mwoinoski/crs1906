"""
Primary definition of a playing card.
"""
from card_library.card_constants import Rank, Suit


class PlayingCard:
    """ Define playing cards with rank, suit and face up or down. """
    def __init__(self, rank=None, suit=None, face_card=False):
        upper_rank = 10
        if face_card:
            upper_rank = Rank.KING
        if (rank is None) and not face_card or (rank < Rank.ACE) or (rank > upper_rank):
            raise ValueError(f'A rank between {Rank.ACE} and {upper_rank} must be provided.')
        self.rank = rank
        if (suit is None) or (suit < Suit.CLUBS) or (suit > Suit.SPADES):
            raise ValueError(f'A suit between {Suit.CLUBS} and {Suit.SPADES} must be provided.')
        self.suit = suit
        self.face_up = False

    def flip(self):
        """ Change face up or face down state. """
        self.face_up = not self.face_up

    def __str__(self):
        if not self.face_up:
            return "XX"
        return Rank.chars[self.rank] + Suit.chars[self.suit]


if __name__ == '__main__':
    print("Testing class PlayingCard")
    c1 = PlayingCard(rank=2, suit=Suit.DIAMONDS)
    c1.flip()
    print("ToString is:", c1)
    print("Rank is:", c1.rank)
    print("Suit is:", c1.suit)
    c2 = PlayingCard(Rank.ACE, Suit.SPADES)
    print("Face down ToString is:", c2)
