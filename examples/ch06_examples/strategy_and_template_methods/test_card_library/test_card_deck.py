"""
Class to unit test proper operation of the CardDeck class.
"""
import unittest
from card_library.card_constants import Rank, Suit
from card_library.card_deck import CardDeck
from card_library.shufflers import *


class TestCardDeck(unittest.TestCase):
    """ CardDeck unit test class. """

    def setUp(self):
        """ Always construct a card deck instance before each test. """
        self.deck = CardDeck()

    def test_creation(self):
        """ Ensure card deck object created. """
        self.assertIsNotNone(self.deck)

    def test_full_deck(self):
        """ Ensure that after creation the card deck has exactly 52 cards """
        self.assertEqual(52, self.deck.cards_remaining)

    def test_sorted_deck(self):
        """ Validate deck is sorted after construction. """
        temp = str(self.deck)[0: 14]
        self.assertEqual("A♣ 2♣ 3♣ 4♣ 5♣", temp)

    def test_dealing(self):
        """ Test dealing cards from the deck. """
        card = self.deck.deal()
        self.assertEqual(51, self.deck.cards_remaining)
        self.assertEqual(Rank.KING, card.rank)
        self.assertEqual(Suit.SPADES, card.suit)
        self.assertFalse(card.face_up)
        card = self.deck.deal()
        self.assertEqual(50, self.deck.cards_remaining)

    def test_shuffling(self):
        """ Test shuffling of the deck using a highly-unlikely but not impossible result. """
        self.assertEqual()
        temp = str(self.deck)[0: 14]
        self.assertEqual("A♣ 2♣ 3♣ 4♣ 5♣", temp)
        self.deck.shuffler = SimpleKnuthShuffler()
        self.deck.shuffle()
        temp = str(self.deck)[0: 14]
        self.assertNotEqual("A♣ 2♣ 3♣ 4♣ 5♣", temp)
        self.assertEqual()
        temp = str(self.deck)[0: 14]
        self.assertEqual("A♣ 2♣ 3♣ 4♣ 5♣", temp)
        self.deck.shuffler = ModifiedKnuthShuffler()
        self.deck.shuffle()
        temp = str(self.deck)[0: 14]
        self.assertNotEqual("A♣ 2♣ 3♣ 4♣ 5♣", temp)

