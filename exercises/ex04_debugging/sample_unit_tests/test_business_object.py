"""
mock_demo.py - Test case that uses mock objects, from Chapter 3 examples
"""

import sqlite3

from unittest import TestCase
from unittest.mock import Mock
from person import Person
from business_object import BusinessObject, UserDao, BusinessError


class TestBusinessObject(TestCase):

    def test_get_user(self):
        expected_result = Person('Isaac', None, 'Newton')

        # create a mock for the DAO itself
        mock_dao = Mock(spec=UserDao)
        # create a mock for the DAO's query_user method and
        # set the return value of the mock method
        mock_dao.query_user.return_value = expected_result

        bus_obj = BusinessObject('mock_demo')
        # replace the real DAO with the mock DAO
        bus_obj.user_dao = mock_dao

        user_id = 123
        # when the business method is called, it will use the mock DAO
        # instead of the real DAO
        actual_result = bus_obj.get_user(user_id)

        # verify that the mock method was called correctly
        mock_dao.query_user.assert_called_with(user_id)
        # verify that the actual result equals the expected result
        self.assertEqual(expected_result, actual_result)

    def test_get_user_not_found(self):
        mock_dao = Mock(spec=UserDao)
        mock_dao.query_user = Mock()
        mock_dao.query_user.return_value = None

        bus_obj = BusinessObject('mock_demo')
        bus_obj.user_dao = mock_dao

        user_id = 123
        with self.assertRaisesRegex(ValueError, r'[Vv]alid.*[Ii][Dd]'):
            bus_obj.get_user(user_id)

        mock_dao.query_user.assert_called_with(user_id)

    def test_get_user_dao_error(self):
        mock_dao = Mock(spec=UserDao)
        # Configure the mock query_user method to raise a DB error
        mock_dao.query_user = Mock(side_effect=sqlite3.Error('SQL error'))

        bus_obj = BusinessObject('mock_demo')
        bus_obj.user_dao = mock_dao

        user_id = 123
        with self.assertRaisesRegex(BusinessError, 'SQL error'):
            bus_obj.get_user(user_id)

        mock_dao.query_user.assert_called_with(user_id)
