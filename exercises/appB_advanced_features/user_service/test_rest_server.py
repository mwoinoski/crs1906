"""
Integration tests for rest_server.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import json
import requests

user_ned = {
    "email": "ned.flanders@gmail.com",
    "first_name": "Ned",
    "middles": "Abraham",
    "last_name": "Flanders",
    "address": {
        "street": "125 Maple St",
        "post_code": "97478",
        "city": "Springfield",
        "state": "OR",
        "country": "USA",
    }
}

user_miles = {
    "email": "miles@jazz.com",
    "first_name": "Miles",
    "middles": None,
    "last_name": "Davis",
    "address": {
        "country": "USA",
        "street": "5311 E 1st St",
        "city": "New York",
        "post_code": "10012",
        "state": "NY"
    }
}

base_url = 'http://localhost:5000/rest/users'


def test_get_user_found():
    email = 'ned.flanders@gmail.com'
    url = '{}/{}'.format(base_url, email)
    creds = ('student', 'studentpw')
    http_headers = {'Accept': 'application/json'}

    r = requests.get(url, auth=creds, headers=http_headers)

    actual_result = r.json()

    print('GET {} status {}, response = {}'
          .format(url, r.status_code, actual_result))

    assert r.status_code == 200

    assert actual_result == {'user': user_ned}


def test_get_user_not_found():
    url = '{}/{}'.format(base_url, 'nobody@nowhere.com')
    headers = {'Accept': 'application/json'}
    creds = ('student', 'studentpw')

    r = requests.get(url, auth=creds, headers=headers)

    assert r.status_code == 404


def test_add_user_ok():
    url = base_url
    http_headers = {'Content-Type': 'application/json'}
    creds = ('student', 'studentpw')

    r = requests.post(url, auth=creds, headers=http_headers, json=user_miles)

    actual_result = r.json()

    print('POST {} status {}'.format(url, r.status_code))
    assert r.status_code == 201

    assert actual_result == {'user': user_miles}


def test_update_user_ok():
    email = 'miles@jazz.com'
    url = '{}/{}'.format(base_url, email)
    http_headers = {'Content-Type': 'application/json'}
    creds = ('student', 'studentpw')

    expected_result = dict(user_miles)
    expected_result['middles'] = 'Dewey'
    expected_result['address']['post_code'] = '10013'

    r = requests.put(url, auth=creds, headers=http_headers,
                     json=expected_result)

    print('PUT {} status {}'.format(url, r.status_code))
    assert r.status_code == 202

    actual_result = r.json()
    assert actual_result == {'user': expected_result}


def test_delete_user_found():
    url = '{}/{}'.format(base_url, 'miles@jazz.com')
    creds = ('student', 'studentpw')

    r = requests.delete(url, auth=creds)

    print('DELETE {} status {}'.format(url, r.status_code))

    assert r.status_code == 204


def test_delete_user_not_found():
    url = '{}/{}'.format(base_url, 'nobody@nowhere.com')
    creds = ('student', 'studentpw')

    r = requests.delete(url, auth=creds)

    assert r.status_code == 404
