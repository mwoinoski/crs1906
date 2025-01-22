"""
Game hand to manipulate cards for each player.
"""
from card_library.card_deck import CardDeck


class GameHand:
    """ GameHand class definition. """
    def __init__(self):
        self.__cards = []

    def insert(self, card):
        """ Insert a playing card into the hand. """
        card.face_up = True
        self.__cards.append(card)

    def return_cards_to_deck(self, deck_in_use):
        """ Return all cards in the hand to the deck. """
        for card in self.__cards:
            deck_in_use.insert(card)
        self.__cards = []

    @property
    def cards(self):
        """ Provide read-only access to the cards in the hand. """
        return self.__cards

    @property
    def card_count(self):
        """ Provide read-only access to the number of cards in the hand. """
        return len(self.__cards)

    def __str__(self):
        rep = ""
        for card in self.__cards:
            rep += str(card) + " "
        return rep


if __name__ == '__main__':
    print("Testing class GameHand")
    deck = CardDeck()
    deck.shuffle()
    hand = GameHand()
    for i in range(0, 5):
        hand.insert(deck.deal())
    print("Show random cards in the hand with count of 5 after dealing")
    print("Hand is:", hand, hand.card_count)
    print("Deck count should be 47", deck.cards_remaining)
    hand.return_cards_to_deck(deck)
    print("Show no cards hand in the hand and deck at 52")
    print("Hand is:", hand, hand.card_count)
    print("Deck count count", deck.cards_remaining)
