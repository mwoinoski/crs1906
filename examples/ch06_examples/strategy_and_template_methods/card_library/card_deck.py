"""
Definition of a card deck with shuffle and deal capabilities
Self constructs with playing cards and face cards.
"""
from card_library.card_constants import Rank, Suit
from card_library.playing_card import PlayingCard
from card_library.face_card import FaceCard
from card_library.shufflers import SimpleKnuthShuffler


class CardDeck:
    """ CardDeck class to hold playing and face cards. """
    def __init__(self):
        self.__deck = []
        for suit in range(Suit.CLUBS, Suit.SPADES + 1):
            for rank in range(Rank.ACE, Rank.KING + 1):
                if rank < Rank.JACK:
                    card = PlayingCard(rank, suit)
                else:
                    card = FaceCard(rank, suit)
                card.face_up = True
                self.__deck.append(card)
        self.shuffler = SimpleKnuthShuffler()

    @property
    def cards_remaining(self):
        """ Report number of cards remaining in the deck. """
        return len(self.__deck)

    def deal(self):
        """ Deal a card from the top of the deck (like a stack). """
        card = self.__deck.pop()
        card.face_up = False
        return card

    def insert(self, card):
        """ Return a card back into the deck. """
        card.face_up = True
        self.__deck.append(card)

    def shuffle(self):
        """ Call an algorithm to randomly organize the deck. """
        self.shuffler.shuffle(self.__deck)

    def __str__(self):
        rep = ""
        for card in self.__deck:
            rep += str(card) + " "
        return rep


if __name__ == '__main__':
    def show():
        """ Helper method to show card deck status. """
        print("Tostring is:", deck)
        print("Cards in deck:", deck.cards_remaining)

    print("Testing class CardDeck")
    deck = CardDeck()
    print("\nSorted deck AS should be on top with 52 cards")
    show()

    print("\nShuffle test should show cards in random order")
    deck = CardDeck()
    deck.shuffle()
    show()

    print("\nDealing and inserting test should show 51 then 52 again")
    deck = CardDeck()
    temp = deck.deal()
    show()
    deck.insert(temp)
    show()
