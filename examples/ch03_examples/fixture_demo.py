r"""
fixture_demo.py - Test case that defines a test fixture
"""

import sqlite3

import pytest
from pytest import raises
from unittest.mock import Mock

from person import Person
from business_object import BusinessObject, UserDao, BusinessError


# Define a test fixture. The value returned by the fixture function will
# be passed as an argument to every test case that defines a parameter
# with the same name as the fixture.
@pytest.fixture
def init_mock_fixture():
    return Mock(spec=UserDao)


# The name of the parameter of this test function matches the name of the
# fixture, so pytest will call the fixture and pass its return value as the
# test function's parameter value.
def test_get_user(init_mock_fixture):
    print('\n----------- test_get_user ------------')

    expected_result = Person('Isaac', None, 'Newton')

    # get the mock DAO that was created by the test fixture
    mock_dao = init_mock_fixture
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
    assert expected_result == actual_result


# The init_mock_fixture return value will be passed to this test function
def test_get_user_not_found(init_mock_fixture):
    print('\n----------- test_get_user_not_found ------------')

    # get the mock DAO that was created by the test fixture
    mock_dao = init_mock_fixture
    mock_dao.query_user.return_value = None

    bus_obj = BusinessObject('mock_demo')
    bus_obj.user_dao = mock_dao

    user_id = 123
    with raises(ValueError, match=r'[Vv]alid.*[Ii][Dd]'):
        bus_obj.get_user(user_id)

    mock_dao.query_user.assert_called_with(user_id)


# The init_mock_fixture return value will be passed to this test function
def test_get_user_dao_error(init_mock_fixture):
    print('\n----------- test_get_user_dao_error ------------')

    # get the mock DAO that was created by the test fixture
    mock_dao = init_mock_fixture
    # Configure the mock query_user method to raise a DB error
    mock_dao.query_user.side_effect = sqlite3.Error('SQL error')

    bus_obj = BusinessObject('mock_demo')
    bus_obj.user_dao = mock_dao

    user_id = 123
    with raises(BusinessError, match='SQL error'):
        bus_obj.get_user(user_id)

    mock_dao.query_user.assert_called_with(user_id)
