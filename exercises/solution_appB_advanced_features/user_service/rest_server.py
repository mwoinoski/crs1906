"""
rest_server.py - Simple REST server based on Flask.
"""

# TODO: note the Flask imports
# (no code change required)
from flask import (Flask, jsonify, abort, request, make_response, url_for,
                   Response)
from flask_httpauth import HTTPBasicAuth  # ignore the PyCharm error here

import rest_server_dao


app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


# TODO: note the definition of the Flask authentication callback function
# (no code change required)
@auth.get_password
def get_password(username):
    """Callback function that returns the password for username"""
    return rest_server_dao.get_password(username)


# TODO: note the definition of the Flask error handler for requests without
# valid login credentials
# (no code change required)
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    # Note: if the client is a browser, the 401 cause the browser to
    # display the default auth dialog. But that shouldn't be a problem here
    # because the request will an asynchronous call from JavaScript or a
    # Python client.
    

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# TODO: note the setting of the base URI
# (no code change required)
BASE_URI = '/rest/users'


# TODO: add a Flask decorator here so that a GET request to BASE_URI is mapped
# to the get_users() method below
@app.route(BASE_URI, methods=['GET'])
# TODO: add decorator that specifies the request must include valid credentials
@auth.login_required
def get_users():
    app.logger.info('Getting all users')

    # TODO: note how we delegate the look up of the users to a DAO and
    # assign the list of users to the variable 'users'
    # (no code change required)
    users = rest_server_dao.get_all_users()

    # TODO: return a jsonified dictionary with key of 'users' and value of
    # the users list
    return jsonify({'users': users})


# TODO: add a Flask decorator here so that a GET request
# to BASE_URI+'/<email>' is mapped to the get_user() method below.
@app.route(BASE_URI + '/<string:email>', methods=['GET'])
# TODO: add decorator that specifies the request must include valid credentials
@auth.login_required
def get_user(email):
    app.logger.info('Getting user %s', email)

    # TODO: note how we delegate the look up of the user to a DAO and
    # assign the user to the variable 'user'
    # (no code change required)
    user = rest_server_dao.get_user(email)

    # TODO: if user is None, abort with HTTP status 404
    if user is None:
        abort(404)

    # TODO: return a jsonified dictionary with key of 'user' and value of
    # the user
    return jsonify({'user': user})


# TODO: add a decorator so a POST request to BASE_URI is mapped create_users()
@app.route(BASE_URI, methods=['POST'])
# TODO: add decorator that specifies the request must include valid credentials
@auth.login_required
def create_user():
    # TODO: add a test to ensure that the request body contains JSON and
    # the JSON has a member named 'email'. Abort with status 400 if the
    # test fails.
    if not request.json or 'email' not in request.json:
        app.logger.error('No email in POST request to create user')
        abort(400)

    # TODO: get the email from the request JSON and assign it to a variable
    # named 'email'
    email = request.json['email']
    app.logger.info('Creating user %s', email)

    # TODO: note how we get the rest of the input data from the request
    # (no code change required)
    first_name = request.json.get('first_name', '')
    middles = request.json.get('middles', '')
    last_name = request.json.get('last_name', '')
    street = request.json['address'].get('street', '')
    post_code = request.json['address'].get('post_code', '')
    city = request.json['address'].get('city', '')
    state = request.json['address'].get('state', '')
    country = request.json['address'].get('country', '')

    # TODO: note how we delegate the creation of the user to a DAO and
    # assign the new user to the variable 'user'
    # (no code change required)
    user = rest_server_dao.create_user(email, first_name, middles, last_name,
                                       street, post_code, city, state, country)

    # TODO: return two values:
    # 1. a jsonified dictionary with key of 'user' and value of the new user
    # 2. HTTP status 201
    return jsonify({'user': user}), 201  # 201 == Created


# TODO: add a Flask decorator here so that a PUT request
# to BASE_URI+'/<email>' is mapped to the update_user() method below.
@app.route(BASE_URI + '/<string:email>', methods=['PUT'])
# TODO: add decorator that specifies the request must include valid credentials
@auth.login_required
def update_user(email):
    # TODO: add a test to ensure that the request body contains JSON.
    # Abort with status 400 if the test fails.
    if not request.json:
        app.logger.error('No JSON in PUT request to update user %s', email)
        abort(400)

    # TODO: get the email from the request JSON and assign it to a variable
    # named 'email'
    email = request.json['email']
    app.logger.info('Updating user %s', email)

    # TODO: note how we get the rest of the input data from the request
    # (no code change required)
    first_name = request.json.get('first_name', '')
    middles = request.json.get('middles', '')
    last_name = request.json.get('last_name', '')
    street = request.json['address'].get('street', '')
    post_code = request.json['address'].get('post_code', '')
    city = request.json['address'].get('city', '')
    state = request.json['address'].get('state', '')
    country = request.json['address'].get('country', '')

    # TODO: note how we delegate the update of the user to a DAO and
    # assign the modified user to the variable 'user'
    # (no code change required)
    user = rest_server_dao.update_user(email, first_name, middles, last_name,
                                       street, post_code, city, state, country)

    # TODO: if user is None, abort with HTTP status 404
    if user is None:
        app.logger.error("User %s not found, can't update", email)
        abort(404)

    # TODO: return two values:
    # 1. a jsonified dictionary with key of 'user' and value of the new user
    # 2. HTTP status 202
    return jsonify({'user': user}), 202  # 202 == Accepted


# TODO: add a Flask decorator here so that a DELETE request
# to BASE_URI+'/<email>' is mapped to the delete_user() method below.
@app.route(BASE_URI + '/<string:email>', methods=['DELETE'])
# TODO: add decorator that specifies the request must include valid credentials
@auth.login_required
def delete_user(email):
    app.logger.info('Deleting user %s', email)

    # TODO: note how we delegate the deletion of the user to a DAO.
    # (no code change required)
    if not rest_server_dao.delete_user(email):
        app.logger.error("User %s not found, can't delete", email)
        abort(404)

    # TODO: return HTTP response 204
    return Response(status=204)  # 204 == No Content


def make_public_user(user):
    """
    Add a uri attribute to a task.

    The client uses the task's URI to perform operations on the task by
    accessing the uri with HTTP GET, PUT, or DELETE. This is a more RESTful
    technique than relying on a primary key from the database, because the
    URI does not need to map directly to an implementation artifact. The URI
    is simply a hyperlink; if the location of the task later changes, the
    client can still use the original URI, and the service can map the URI to
    the new resource location.
    """
    new_user = {}
    for field in user:
        if field == 'email':
            # Add a uri field to the returned record.
            new_user['uri'] = url_for('get_user', email=user['email'],
                                      _external=True)
        new_user[field] = user[field]
    return new_user


if __name__ == '__main__':
    app.run(debug=True)  # debug=True activates HTML debug messages
