"""
mock_sentinel_demo.py - Test case that uses mock.sentinel,
from Chapter 3 examples
"""

import unittest
import unittest.mock
from unittest import TestCase
from unittest.mock import patch, sentinel
from business_object import BusinessObject, UserDao


class TestBusinessObject(TestCase):

    @patch.object(UserDao, 'query_user')
    def test_get_user(self, mock_query_user_method):
        # no need to create a Person, just use Mock's sentinel
        # as a generic object

        # BusinessObject.get_user references Person.last_name, so add a
        # person attribute, which has a last_name attribute, to the sentinel
        sentinel.person.last_name = 'Jackson'
        # Tell the mock query_user method to return the sentinel
        mock_query_user_method.return_value = sentinel.person

        bus_obj = BusinessObject('mock_demo')

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_query_user_method.assert_called_with(user_id)
        self.assertEqual(sentinel.person, actual_result)

    @patch('business_object.UserDao')
    def test_get_user_skip_dao_constructor(self, mock_user_dao_class):
        mock_class = mock_user_dao_class.return_value
        # no need to create a Person, just use Mock's sentinel
        sentinel.person.last_name = 'Lincoln'
        mock_class.query_user.return_value = sentinel.person
        bus_obj = BusinessObject('mock_demo')

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_class.query_user.assert_called_with(user_id)
        self.assertEqual(sentinel.person, actual_result)
