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

import requests

# if you want the test cases to run in a different order, assign a new function
# for comparing method names to TestLoader's sortTestMethodsUsing attribute:
#     unittest.defaultTestLoader.sortTestMethodsUsing = \
#         lambda x, y: -1 if x < y else 1 if x > y else 0

user_ned_xml = """
    <user>
        <email>ned.flanders@gmail.com</email>
        <first_name>Ned</first_name>
        <middles>Abraham</middles>
        <last_name>Flanders</last_name>
        <address>
            <country>USA</country>
            <post_code>97478</post_code>
            <street>125 Maple St</street>
            <state>OR</state>
            <city>Springfield</city>
        </address>
    </user>
"""

user_miles_xml = """
    <user>
        <email>miles@jazz.com</email>
        <first_name>Miles</first_name>
        <middles></middles>
        <last_name>Davis</last_name>
        <address>
            <country>USA</country>
            <street>5311 E 1st St</street>
            <city>New York</city>
            <post_code>10012</post_code>
            <state>NY</state>
        </address>
    </user>
"""

# TODO: note that base_url will be used for all REST requests
# (no code change required)
base_url = 'http://localhost/rest/users'


def test_get_user_found():
    # TODO: you'll look up a user with GET request like this:
    # GET http://localhost/rest/users/ned.flanders@gmail.com
    # The GET request will return XML data.
    # (no code change required)

    email = 'ned.flanders@gmail.com'

    # TODO: build the URL for the GET request from base_url and email
    url = '{}/{}'.format(base_url, email)

    # TODO: set the HTTP Accept header to 'application/xml'
    http_headers = {'Accept': 'application/xml'}

    # TODO: send the GET request and store the result in a variable named 'r'
    r = requests.get(url, headers=http_headers)

    # TODO: get the XML from the response body and assign it to a variable
    # named 'actual_result'
    actual_result = r.text

    print('GET {} status {}, response = {}'
          .format(url, r.status_code, actual_result))

    # parse XML in response body

    # TODO: note the assertions that test the result of the REST request
    # (no code change required)
    assert r.status_code == 200
    # assert actual_result == user_ned_xml  # FIXME


def test_get_user_not_found():
    url = '{}/{}'.format(base_url, 'nobody@nowhere.com')
    headers = {'Accept': 'application/xml'}

    r = requests.get(url, headers=headers)

    assert r.status_code == 404


def test_add_user_ok():
    # TODO: you'll add a new user with a POST request like this:
    # POST http://localhost/rest/users
    # { "email": "miles@jazz.com", "first_name": "Miles", etc. }
    # (no code change required)

    # TODO: set the url to base_url
    url = base_url

    # TODO: set the HTTP Accept header to 'application/xml'
    http_headers = {'Content-Type': 'application/xml'}

    # TODO: send the POST request and store the result in a variable named 'r'
    r = requests.post(url, headers=http_headers, data=user_miles_xml.strip())

    print('POST {} status {}'.format(url, r.status_code))

    # TODO: note the assertion that tests the result of the REST request
    # (no code change required)
    assert r.status_code == 201


def test_update_user_ok():
    user_miles_xml['middles'] = 'Dewey'  # FIXME
    user_miles_xml['address']['zipcode'] = '10013'  # FIXME

    # TODO: you'll update an existing user with a PUT request like this:
    # PUT http://localhost/rest/users
    # { "email": "miles@jazz.com", "first_name": "Miles", etc. }
    # (no code change required)

    # TODO: set the url to base_url
    url = base_url

    # TODO: send the PUT request and store the result in a variable named 'r'
    r = requests.put(url, data=user_miles_xml.strip())

    print('PUT {} status {}'.format(url, r.status_code))

    # TODO: note the assertion that tests the result of the REST request
    # (no code change required)
    assert r.status_code == 202


def test_delete_user_not_found():
    url = '{}/{}'.format(base_url, 'nobody@nowhere.com')

    r = requests.delete(url)

    assert r.status_code == 404
