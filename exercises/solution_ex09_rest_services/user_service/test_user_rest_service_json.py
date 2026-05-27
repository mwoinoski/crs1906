r"""
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

import requests

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

# if you want the test cases to run in a different order, assign a new function
# for comparing method names to TestLoader's sortTestMethodsUsing attribute:
#     unittest.defaultTestLoader.sortTestMethodsUsing = \
#         lambda x, y: -1 if x < y else 1 if x > y else 0

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

base_url = 'http://localhost:6544/rest/users'
creds = ('admin', 'adminpw')


def test_get_user_found():
    email = 'ned.flanders@gmail.com'
    url = f'{base_url}/{email}'
    http_headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=http_headers, auth=creds)

    actual_result = response.json()

    print(f'GET {url} status {response.status_code}, response = {actual_result}')

    # The service returns a wrapped payload: {'user': {...}}
    actual_user = actual_result['user']

    # update our expected user with fields populated by the service
    user_ned['id'] = actual_user['id']
    user_ned['username'] = actual_user['username']
    user_ned['password'] = actual_user['password']

    assert response.status_code == 200
    assert actual_user == user_ned


def test_get_user_not_found():
    url = f'{base_url}/nobody@nowhere.com'
    http_headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=http_headers, auth=creds)

    assert response.status_code == 404


def test_add_user_ok():
    url = base_url
    http_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=http_headers, json=user_miles, auth=creds)

    print(f'POST status {response.status_code}')

    assert response.status_code == 201


def test_update_user_ok():
    user_miles['middles'] = 'Dewey'
    user_miles['address']['zipcode'] = '10013'

    url = f"{base_url}/{user_miles['email']}"
    http_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.put(url, headers=http_headers, json=user_miles, auth=creds)

    print(f'PUT status {response.status_code}')

    assert response.status_code == 202


def test_delete_user_not_found():
    url = f'{base_url}/nobody@nowhere.com'

    response = requests.delete(url, auth=creds)

    assert response.status_code == 404
