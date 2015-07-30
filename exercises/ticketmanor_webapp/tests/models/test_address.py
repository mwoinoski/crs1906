"""
Unit tests for Address

   Run as follows:
   cd TicketManor
   python -m unittest ticketmanor/tests/person_test.py
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import unittest

from ticketmanor.models.address import Address

class AddressTestCase(unittest.TestCase):
    """Unit tests for Address"""

    def test_eq_instances_eq(self):
        a1 = AddressTestCase.create_address()
        a2 = AddressTestCase.create_address()
        self.assertEqual(a1, a2)

    def test_eq_instances__ne(self):
        a1 = AddressTestCase.create_address()
        a2 = AddressTestCase.create_address()
        a2.post_code = "2"
        self.assertNotEqual(a1, a2)

    def test_eq_instances_eq_operator(self):
        a1 = AddressTestCase.create_address()
        a2 = AddressTestCase.create_address()
        self.assertTrue(a1 == a2)

    def test_eq_instances__ne_operator(self):
        a1 = AddressTestCase.create_address()
        a2 = AddressTestCase.create_address()
        a2.post_code = "2"
        self.assertTrue(a1 != a2)

    @staticmethod
    def create_address():
        return Address(
            street="123 Main St",
            city="Eden",
            state="Garden",
            country="Paradise",
            post_code="1",
        )

if __name__ == '__main__':
    unittest.main()
