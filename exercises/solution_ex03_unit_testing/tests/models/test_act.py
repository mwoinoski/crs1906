"""
test_act.py - Unit tests for Act class
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase
from ticketmanor.models.act import Act


class TestAct(TestCase):

    def test_act_type_int(self):
        self.assertEqual(Act.MOVIE,
                         Act.ACT_TYPE_INV[Act.ACT_TYPE[Act.MOVIE]])
        self.assertEqual(Act.MUSIC,
                         Act.ACT_TYPE_INV[Act.ACT_TYPE[Act.MUSIC]])
        self.assertEqual(Act.THEATER,
                         Act.ACT_TYPE_INV[Act.ACT_TYPE[Act.THEATER]])
        self.assertEqual(Act.SPORTS,
                         Act.ACT_TYPE_INV[Act.ACT_TYPE[Act.SPORTS]])

