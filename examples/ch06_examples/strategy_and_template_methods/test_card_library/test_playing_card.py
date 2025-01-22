"""
Unit test logic to validate class PlayingCard.
"""
import unittest
from card_library.card_constants import Rank, Suit
from card_library.playing_card import PlayingCard


class TestPlayingCard(unittest.TestCase):
    """ Main test class. """

    def setUp(self) -> None:
        """ Test that etup always creates a playing card. """
        self.card = PlayingCard(Rank.ACE, Suit.SPADES)

    def test_creation(self):
        """ Confirm a playing card can be constructed. """
        self.assertIsNotNone(self.card)

    def test_valid_rank(self):
        """ Confirm valid rank was established properly in construction. """
        self.assertEqual(Rank.ACE, self.card.rank)

    def test_valid_suit(self):
        """ Confirm valid suit was established properly in construction. """
        self.assertEqual(Suit.SPADES, self.card.suit)

    def test_invalid_rank(self):
        """ Insure proper exception is thrown if invalid rank is used. """
        with self.assertRaises(ValueError):
            PlayingCard(0, Suit.CLUBS)

    def test_face_rank_in_playing_card(self):
        """ Insure proper exception if face card rank is used in playing card. """
        with self.assertRaises(ValueError):
            PlayingCard(Rank.KING, Suit.DIAMONDS)

    def test_invalid_suit(self):
        """ Insure proper exception if invalid suit is used. """
        with self.assertRaises(ValueError):
            PlayingCard(2, 20)

    def test_to_string(self):
        """ Confirm card properly displays 2-digit card code. """
        self.assertEqual("XX", str(self.card))
        self.card.flip()
        self.assertEqual("A" + Suit.SPADE_SYMBOL, str(self.card))

    def test_flipping(self):
        """ Confirm that flipping a card changes its face-up/down state. """
        self.assertFalse(self.card.face_up)
        self.card.flip()
        self.assertTrue(self.card.face_up)
