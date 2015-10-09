"""
mock_demo.py - Test case that uses the @patch decorator from unittet.mock,
from Chapter 3 examples
"""

from unittest import TestCase, main
from unittest.mock import patch
from person import Person
from models.bus_obj import BusinessObject
from db.user_dao import UserDao


class TestBusinessObject(TestCase):

    # Patch the UserDao.query_user method. The mock for the patched method
    # will be passed as the test method's second argument
    @patch.object(UserDao, 'query_user')
    def test_get_user(self, mock_query_user_method):
        print('\n----------- test_get_user ------------')

        expected_result = Person('Isaac', None, 'Newton')
        # set the return value for the mock method
        mock_query_user_method.return_value = expected_result

        bus_obj = BusinessObject('mock_demo')

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_query_user_method.assert_called_with(user_id)
        self.assertEquals(expected_result, actual_result)

    @patch('models.bus_obj.UserDao')
    # Important: NOT @patch('db.user_dao.UserDao')
    # Patch a class where it's imported, not where it's defined
    def test_get_user_skip_dao_constructor(self, mock_user_dao_class):
        print('\n----- test_get_user_skip_dao_constructor -----')

        mock_dao = mock_user_dao_class.return_value
        print('Type of mock:', mock_dao.__class__.__name__)
        expected_result = Person('Isaac', None, 'Newton')
        mock_dao.query_user.return_value = expected_result

        # BusinessObject constructor's call to UserDao() now creates a mock
        bus_obj = BusinessObject('mock_demo')
        # no need to set BusinessObject's user_dao

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_dao.query_user.assert_called_with(user_id)
        self.assertEquals(expected_result, actual_result)

    @patch('models.bus_obj.UserDao')
    @patch('db.user_dao.Person')
    def test_double_patch(self, mock_person_class, mock_user_dao_class):
        print('\n----- test_double_patch -----')

        mock_dao = mock_user_dao_class.return_value
        print('Type of mock dao:', mock_dao.__class__.__name__)
        mock_person = mock_person_class.return_value
        print('Type of mock person:', mock_person.__class__.__name__)

        expected_result = mock_person
        mock_dao.query_user.return_value = expected_result
        bus_obj = BusinessObject('mock_demo')

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_dao.query_user.assert_called_with(user_id)
        self.assertEquals(expected_result, actual_result)

if __name__ == '__main__':
    main()
