"""
magicmock_demo.py - Example of MagicMock, from Chapter 3
"""

from unittest import TestCase
from unittest.mock import MagicMock
from business_object import Person


# class Department:
#     def __init__(self, name):
#         self.name = name
#         self.persons = {}
#
#     def add_employee(self, person):
#         self.persons[person.id] = person
#
#     def get_employee(self, id):
#         return self.persons[id]


class TestDepartment(TestCase):

    def test_add_employee(self):
        dept = Department('Software Development')
        mock_dict = MagicMock()
        dept.persons = mock_dict

        person = Person(2785, 'Bobby', 'James', 'Fischer')

        dept.add_employee(person)

        mock_dict.__setitem__.assert_called_with(2785, person)

    def test_get_employee(self):
        dept = Department('Software Development')
        mock_dict = MagicMock()
        dept.persons = mock_dict

        expected_result = Person(2690, 'Boris', 'Vasilievich', 'Spassky')
        mock_dict.__getitem__.return_value = expected_result

        actual_result = dept.get_employee(4321)

        self.assertEquals(expected_result, actual_result)

