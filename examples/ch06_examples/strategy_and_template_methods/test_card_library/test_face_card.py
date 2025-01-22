"""
Unit tests to confirm proper operation of the FaceCard class.
"""
import unittest
from card_library.card_constants import Rank, Suit
from card_library.face_card import FaceCard


class TestFaceCard(unittest.TestCase):
    """ FaceCard test class"""

    def setUp(self) -> None:
        """ Always construct a face card before each test. """
        self.card = FaceCard(Rank.JACK, Suit.HEARTS)

    def test_creation(self):
        """ Confirm face card creation in constructor. """
        self.assertIsNotNone(self.card)

    def test_valid_rank(self):
        """ Validate that the proper rank was constructed. """
        self.assertEqual(Rank.JACK, self.card.rank)

    def test_invalid_rank(self):
        """ Insure invalid rank values throw exception. """
        with self.assertRaises(ValueError):
            FaceCard(10, Suit.CLUBS)

    def test_to_string(self):
        """ Validate that face cards display number of eyes. """
        self.assertEqual("XX", str(self.card))
        self.card.flip()
        self.assertEqual("J" + Suit.HEART_SYMBOL + '1', str(self.card))

    def test_eyes(self):
        """ Validate that the correct number of eyes are constructed. """
        self.assertEqual(1, self.card.eyes)
        self.card = FaceCard(Rank.QUEEN, Suit.HEARTS)
        self.assertEqual(2, self.card.eyes)
