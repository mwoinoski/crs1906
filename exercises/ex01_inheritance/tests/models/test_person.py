"""
Unit tests for Person
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import unittest

from ticketmanor.models.person import Person
from ticketmanor.models.address import Address


class PersonTestCase(unittest.TestCase):
    """Unit tests for Person"""

    def test_eq_instances_eq(self):
        p1 = self.create_person()
        p2 = self.create_person()
        self.assertEqual(p1, p2)

    def test_eq_instances_no_address(self):
        p1 = self.create_person()
        p1.address = None
        p2 = self.create_person()
        p2.address = None
        self.assertEqual(p1, p2)

    def test_eq_instances_person_field_ne(self):
        p1 = self.create_person()
        p2 = self.create_person()
        p2.first_name = "Eve"
        self.assertNotEqual(p1, p2)

    def test_eq_instances_address_field_ne(self):
        p1 = self.create_person()
        p2 = self.create_person()
        p2.post_code = "2"
        self.assertNotEqual(p1, p2)

    def test_str(self):
        p = Person(first_name='Adam', last_name='Alpha', email='adam.alpha@gmail.com')

        s = str(p)

        self.assertEqual('Adam Alpha adam.alpha@gmail.com', s)

    # Don't make this method static, because if a test case changes an
    # attribute value, the new value persists to the following test cases
    def create_person(self):
        person = Person(
            first_name="Adam",
            middles="NMI",
            last_name="Alpha",
            email="adam.alpha@gmail.com",
            street="123 Main St",
            city="Eden",
            state="Garden",
            country="Paradise",
            post_code="1",
        )
        return person

if __name__ == '__main__':
    unittest.main()
