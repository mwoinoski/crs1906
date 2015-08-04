"""
Unit tests for func_stats.py
"""
from unittest.case import TestCase

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from func_stats import get_function_stats, add_stats


class TestFuncStats(TestCase):

    def test_add_stats(self):
        expected = [
            ('aaa_func', 40, 5.0),
            ('bbb_func', 30, 10.0),
            ('ccc_func', 20, 20.0),
            ('ddd_func', 0, 0),
        ]

        add_stats('ccc_func', 20, 400)
        add_stats('aaa_func', 40, 200)
        add_stats('ddd_func', 0, 0)
        add_stats('bbb_func', 30, 300)

        actual = get_function_stats()

        print('Actual output = {}'.format(actual))

        self.assertEqual(expected, actual)
