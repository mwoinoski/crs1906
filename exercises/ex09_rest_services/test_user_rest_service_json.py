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

# TODO: note that base_url will be used for all REST requests
#       (no code change required)
base_url = 'http://localhost:6543/rest/users'


def test_get_user_found():
    # TODO: you'll look up a user with GET request like this:
    #       GET http://localhost:6543/rest/users/ned.flanders@gmail.com
    #       The GET request will return JSON data.
    #       (no code change required)

    email = 'ned.flanders@gmail.com'

    # TODO: build the URL for the GET request from base_url and email
    # HINT: see slide 9-35
    url = ....

    # TODO: set the HTTP Accept header to 'application/json'
    http_headers = ....

    # TODO: send the GET request and store the result in a variable named 'response'
    # HINT: you don't need to send authorization credentials.
    response = ....

    # TODO: get the JSON from the response body and assign it to a variable
    #       named 'actual_result'
    actual_result = ....

    print(f'GET {url} status {response.status_code}, response = {actual_result}')

    # update our test user with the id by the database
    user_ned['id'] = actual_result['id']

    # TODO: note the assertions that test the result of the REST request
    #       (no code change required)
    assert response.status_code == 200
    assert actual_result == user_ned

	# TODO: when you have completed the above changes, right-click this file
	#       and select Run 'pytest in test_user_...'. Verify the test case passes.

def test_get_user_not_found():
    url = f'{base_url}/nobody@nowhere.com'
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)

    assert response.status_code == 404



# TODO: After you get the first test case running, uncomment the following 
#       test case and make the required changes. Then run the file again and 
#       verify this second test case passes.

# def test_add_user_ok():
#     # TODO: you'll add a new user with a POST request like this:
#     #       POST http://localhost:6543/rest/users
#     #       { "email": "miles@jazz.com", "first_name": "Miles", etc. }
#     #       (no code change required)
# 
#     # TODO: set the url to base_url
#     ....
# 
#     # TODO: set the HTTP Accept header to 'application/json'
#     ....
# 
#     # TODO: send the POST request and store the result in a variable named `response`
#     #       Pass the the dictionary named user_miles as the JSON data
#     # HINT: you don't need to send authorization credentials.
#     # HINT: see slide 9-36
#     response = ....
# 
#     print(f'POST status {response.status_code}')
# 
#     # TODO: note the assertion that tests the result of the REST request
#     #       (no code change required)
#     assert response.status_code == 201


# TODO: uncomment the following function, make the required changes,
#       and verify this third test case passes.

# def test_update_user_ok():
#     user_miles['middles'] = 'Dewey'
#     user_miles['address']['zipcode'] = '10013'
# 
#     # TODO: you'll update an existing user with a PUT request like this:
#     #       PUT http://localhost:6543/rest/users
#     #       { "email": "miles@jazz.com", "first_name": "Miles", etc. }
#     #       (no code change required)
# 
#     # TODO: set the url to base_url
#     ....
# 
#     # TODO: send the PUT request and store the result in a variable named 'response'
#     #       Pass the the dictionary named user_miles as the JSON data
#     # HINT: you don't need to send authorization credentials.
#     # HINT: see slide 9-37
#     response = ....
# 
#     print(f'PUT status {response.status_code}')
# 
#     # TODO: note the assertion that tests the result of the REST request
#     #       (no code change required)
#     assert response.status_code == 202


def test_delete_user_not_found():
    url = f'{base_url}/nobody@nowhere.com'

    response = requests.delete(url)

    assert response.status_code == 404
