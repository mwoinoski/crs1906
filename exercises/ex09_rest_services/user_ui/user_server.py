"""
user_server.py - Simple REST server based on Flask.
"""

from flask import (Flask, jsonify, abort, request, make_response, url_for,
                   Response)
from flask_httpauth import HTTPBasicAuth  # ignore the PyCharm error here

from user_dao import UserDao

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

dao = UserDao()  # create a Data Access Object (DAO) for database operations


@auth.get_password
def get_password(username):
    """Callback function that returns the password for username"""
    return dao.get_password(username)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    # Note: if the client is a browser, the 401 cause the browser to
    # display the default auth dialog. But that shouldn't be a problem here
    # because the request will an asynchronous call from JavaScript or a
    # Python client.


# noinspection PyUnusedLocal
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


BASE_URI = '/rest/users'


@app.route(BASE_URI, methods=['GET'])
@auth.login_required
def get_users():
    app.logger.info('Getting all users')

    users = dao.get_all_users()

    return jsonify({'users': users})


@app.route(f'{BASE_URI}/<string:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    app.logger.info('Getting user %s', user_id)

    user = dao.get_user(user_id)

    if user is None:
        abort(404)

    return jsonify({'user': user})


@app.route(BASE_URI, methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or 'email' not in request.json:
        app.logger.error('No email in POST request to create user')
        abort(400)

    email = request.json['email']
    app.logger.info('Creating user %s', email)

    username = request.json.get('username', '')
    password = request.json.get('password', '')
    first_name = request.json.get('first_name', '')
    middles = request.json.get('middles', '')
    last_name = request.json.get('last_name', '')
    if 'address' in request.json:
        street = request.json['address'].get('street', '')
        post_code = request.json['address'].get('post_code', '')
        city = request.json['address'].get('city', '')
        state = request.json['address'].get('state', '')
        country = request.json['address'].get('country', '')
    else:
        street = post_code = city = state = country = ''

    user = dao.create_user(
        username, password, email, first_name, middles, last_name, street,
        post_code, city, state, country)

    return jsonify({'user': user}), 201  # 201 == Created


@app.route(f'{BASE_URI}/<string:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    if not user_id:
        app.logger.error('User id is required to update a user')
        abort(400)

    if not request.json:
        app.logger.error('No JSON in PUT request to update user %s', user_id)
        abort(400)

    app.logger.info('Updating user %s', user_id)

    email = request.json.get('email', None)
    first_name = request.json.get('first_name', None)
    middles = request.json.get('middles', None)
    last_name = request.json.get('last_name', None)
    if 'address' in request.json:
        street = request.json['address'].get('street', '')
        post_code = request.json['address'].get('post_code', '')
        city = request.json['address'].get('city', '')
        state = request.json['address'].get('state', '')
        country = request.json['address'].get('country', '')
    else:
        street = post_code = city = state = country = ''

    user = dao.update_user(user_id, email, first_name, middles, last_name,
                           street, post_code, city, state, country)

    if user is None:
        app.logger.error("User %s not found, can't update", user_id)
        abort(404)

    return jsonify({'user': user}), 202  # 202 == Accepted


@app.route(f'{BASE_URI}/<string:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    app.logger.info('Deleting user %s', user_id)

    if not dao.delete_user(user_id):
        app.logger.error("User %s not found, can't delete", user_id)
        abort(404)

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


original_db_file = dao.sqlite_file_name


@app.route(BASE_URI, methods=['PATCH'])
@auth.login_required
def select_db_file():
    """ Allow test cases to switch to a stub database file """
    db_file = request.args.get('db_file')
    if db_file:
        app.logger.info('Switching to database file %s', db_file)
        dao.sqlite_file_name = db_file
    else:
        app.logger.info('Switching base to production database file %s',
                        original_db_file)
        dao.sqlite_file_name = original_db_file
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # debug=True activates HTML debug messages
