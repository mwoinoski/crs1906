"""
Definition of a face card, inherited from playing card to add 'eyes'.
"""
from card_library.card_constants import Rank, Suit
from card_library.playing_card import PlayingCard


class FaceCard(PlayingCard):
    """ FaceCard class for playing cards with 'eyes'. """
    def __init__(self, rank, suit):
        if (rank < Rank.JACK) or (rank > Rank.KING):
            raise ValueError(f'A rank value between {Rank.JACK} and {Rank.KING} must be provided.')
        super().__init__(rank, suit, face_card=True)
        self.__eyes = 2
        if (self.rank == Rank.JACK) and (suit == Suit.HEARTS):
            self.__eyes = 1
        elif (self.rank == Rank.JACK) and (suit == Suit.SPADES):
            self.__eyes = 1
        elif (self.rank == Rank.KING) and (suit == Suit.DIAMONDS):
            self.__eyes = 1

    @property
    def eyes(self):
        """ Primary face card difference is number of eyes. """
        return self.__eyes

    def __str__(self):
        if self.face_up:
            return super().__str__() + str(self.__eyes)
        return super().__str__()


if __name__ == '__main__':
    print("Testing class FaceCard")
    f1 = FaceCard(Rank.JACK, Suit.HEARTS)
    f1.flip()
    print("ToString one eye is:", f1)
    f2 = FaceCard(Rank.KING, Suit.SPADES)
    f2.flip()
    print("ToString two eye is:", f2)
    f2.flip()
    print("ToString face down is:", f2)
