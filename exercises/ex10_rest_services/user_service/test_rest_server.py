"""
Integration tests for UserServiceRest.

These tests cases make several assumptions:
1. A web server is listening on a certain port
2. The TicketManor web app is deployed on that web server
3. The test cases will run in a specific order
In practice, these assumptions are all difficult to guarantee, which results in
a test suite that is brittle, difficult to fully automate, and high-maintenance.

For a more practical approach to integration testing of REST services,
see TicketManor's REST integration tests in
C:\crs1906\exercises\ticketmanor_webapp\tests\rest_services.
The TicketManor integration tests take advantage of Pyramid and SQLite
features that make the tests much more robust and reliable.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import json
import requests

# if you want the test cases to run in a different order, assign a new function
# for comparing method names to the TestLoader's sortTestMethodsUsing attribute.
# unittest.defaultTestLoader.sortTestMethodsUsing = \
#     lambda x, y: -1 if x < y else 1 if x > y else 0

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
    },
}

base_url = 'http://localhost:5000/rest/users'


def test_020_get_user_found():
    url = '{}/{}'.format(base_url, 'miles@jazz.com')
    headers = {'Accept': 'application/json'}

    r = requests.get(url, headers=headers)

    actual_result = r.json  # converts JSON in response to a Python dictionary
    print('GET {} status {}, response = {}'
          .format(url, r.status_code, actual_result))

    # update our test user with the auto-generated id
    user_miles['id'] = actual_result['id']

    assert r.status_code == 200
    assert actual_result == user_miles


def test_020_get_user_not_found():
    url = '{}/{}'.format(base_url, 'nobody@nowhere.com')
    headers = {'Accept': 'application/json'}

    r = requests.get(url, headers=headers)

    assert r.status_code == 404


def test_010_add_user_ok():
    url = base_url
    http_headers = {'Content-type': 'application/json'}

    json_data = json.dumps(user_miles)

    r = requests.post(url, headers=http_headers, data=json_data)

    print('POST {} status {}'.format(url, r.status_code))

    assert r.status_code == 201


def test_030_update_user_ok():
    url = base_url
    user_miles['middles'] = 'Dewey'
    user_miles['address']['zipcode'] = '10013'

    r = requests.put_json(url, data=user_miles)

    print('PUT {} status {}, response = {}'
          .format(url, r.status_code, r.json))

    assert r.status_code == 202
    assert r.json == user_miles

    # Verify user was updated
    url = '{}/{}'.format(base_url, 'miles@jazz.com')
    http_headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=http_headers)
    assert r.status_code == 200
    assert r.json == user_miles


def test_040_delete_user_found():
    url = '{}/{}'.format(base_url, 'miles@jazz.com')

    r = requests.delete(url)

    print('DELETE {} status {}'.format(url, r.status_code))

    assert r.status_code == 204

    # Verify user was deleted
    http_headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=http_headers)
    assert r.status_code == 404


def test_040_delete_user_not_found():
    url = '{}/{}'.format(base_url, 'nobody@nowhere.com')

    r = requests.delete(url)

    assert r.status_code == 404
