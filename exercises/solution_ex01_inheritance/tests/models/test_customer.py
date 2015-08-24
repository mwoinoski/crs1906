"""
Unit tests for Customer

   Run as follows:
   cd TicketManor
   python -m unittest ticketmanor/tests/customer_test.py
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import unittest

from ticketmanor.models.customer import Customer
from ticketmanor.models.address import Address


class CustomerTestCase(unittest.TestCase):
    """Unit tests for Customer"""

    def test_eq_new_instances_eq(self):
        p1 = Customer('Elizabeth', 'Helen', 'Blackburn')
        p2 = Customer('Elizabeth', 'Helen', 'Blackburn')
        self.assertEqual(p1, p2)

    def test_eq_instances_eq(self):
        p1 = self.create_customer()
        p2 = self.create_customer()
        self.assertEqual(p1, p2)

    def test_eq_instances_no_address(self):
        p1 = self.create_customer()
        p1.address = None
        p2 = self.create_customer()
        p2.address = None
        self.assertEqual(p1, p2)

    def test_eq_instances_person_field_ne(self):
        p1 = self.create_customer()
        p2 = self.create_customer()
        p2.first_name = "Eve"
        self.assertNotEqual(p1, p2)

    def test_eq_instances_address_field_ne(self):
        p1 = self.create_customer()
        p2 = self.create_customer()
        p2.post_code = "2"
        self.assertNotEqual(p1, p2)

    def create_customer(self):
        return Customer(
            first_name="Adam",
            middles="Enoch",
            last_name="Alpha",
            email="adam.alpha@gmail.com",
            street="123 Main St",
            city="Eden",
            state="Garden",
            country="Paradise",
            post_code="1",
            customer_id="0001",
        )

if __name__ == '__main__':
    unittest.main()
