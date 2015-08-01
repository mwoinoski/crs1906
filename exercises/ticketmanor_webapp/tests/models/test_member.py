"""
Unit tests for Member

   Run as follows:
   cd TicketManor
   python -m unittest ticketmanor/tests/member_test.py
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import unittest

from ticketmanor.models.member import Member
from ticketmanor.models.address import Address

class MemberTestCase(unittest.TestCase):
    """Unit tests for Member"""

    def test_eq_new_instances_eq(self):
        p1 = Member()
        p2 = Member()
        self.assertEqual(p1, p2)

    def test_eq_instances_eq(self):
        p1 = self.create_member()
        p2 = self.create_member()
        self.assertEqual(p1, p2)

    def test_eq_instances_no_address(self):
        p1 = self.create_member()
        p1.address = None
        p2 = self.create_member()
        p2.address = None
        self.assertEqual(p1, p2)

    def test_eq_instances_person_field_ne(self):
        p1 = self.create_member()
        p2 = self.create_member()
        p2.first_name = "Eve"
        self.assertNotEqual(p1, p2)

    def test_eq_instances_address_field_ne(self):
        p1 = self.create_member()
        p2 = self.create_member()
        p2.post_code = "2"
        self.assertNotEqual(p1, p2)

    def create_member(self):
        return Member(
            id=1,
            first_name="Adam",
            middles="Enoch",
            last_name="Alpha",
            email="adam.alpha@gmail.com",
            address=Address(
                street="123 Main St",
                city="Eden",
                state="Garden",
                country="Paradise",
                post_code="1",
            )
        )

if __name__ == '__main__':
    unittest.main()
