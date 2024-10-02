r"""
Integration tests that do not require any non-standard modules.

These tests cases use the urllib_wrapper module that is defined in this
directory, rather than the non-standard `requests` module. This is useful
in projects where you are restricted from installing modules from PyPI.
"""

import urllib_wrapper


__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


user_ned = {
    "email": "ned.flanders@gmail.com",
    "first_name": "Ned",
    "middles": "Abraham",
    "last_name": "Flanders",
    "address": {
        "country": "USA",
        "post_code": "97478",
        "street": "125 Maple St",
        "state": "OR",
        "city": "Springfield"
    }
}

user_miles = {
    "email": "miles@jazz.com",
    "first_name": "Miles",
    "middles": "",
    "last_name": "Davis",
    "address": {
        "country": "USA",
        "street": "5311 E 1st St",
        "city": "New York",
        "post_code": "10012",
        "state": "NY"
    }
}

base_url = 'http://localhost:6543/rest/users'


def test_get_user_found():
    email = 'ned.flanders@gmail.com'
    url = f'{base_url}/{email}'
    http_headers = {'Accept': 'application/json'}

    response = urllib_wrapper.get(url, headers=http_headers)

    actual_result = response.json()

    # update our test user with the id by the database
    user_ned['id'] = actual_result['id']

    assert response.status_code == 200
    assert actual_result == user_ned


def test_get_user_not_found():
    url = f'{base_url}/nobody@nowhere.com'
    http_headers = {'Accept': 'application/json'}

    response = urllib_wrapper.get(url, headers=http_headers)

    assert response.status_code == 404


def test_add_user_ok():
    url = base_url
    http_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = urllib_wrapper.post(url, headers=http_headers, json=user_miles)

    assert response.status_code == 201


def test_update_user_ok():
    user_miles['middles'] = 'Dewey'
    user_miles['address']['zipcode'] = '10013'

    url = base_url
    http_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = urllib_wrapper.put(url, headers=http_headers, json=user_miles)

    assert response.status_code == 202


def test_delete_user_not_found():
    url = f'{base_url}/nobody@nowhere.com'

    response = urllib_wrapper.delete(url)

    assert response.status_code == 404


