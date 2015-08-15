"""
rest_server.py - Simple REST server based on Flask.
"""

from flask import (Flask, jsonify, abort, request, make_response, url_for,
                   Response)
from flask.ext.httpauth import HTTPBasicAuth

import rest_server_dao


app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    """Callback function that returns the password for username"""
    return rest_server_dao.get_password(username)


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


def make_public_user(user):
    """Add a uri attribute to a user.

    The client uses the user's uri to perform operations on the user by
    accessing the uri with HTTP GET, PUT, or DELETE."""
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id=user['id'],
                                      _external=True)
        else:
            new_user[field] = user[field]
    return new_user


BASE_URI = '/rest/users'


@app.route(BASE_URI, methods=['GET'])
@auth.login_required
def get_users():
    app.logger.info('Getting all users')
    users = [make_public_user(user)
             for user in rest_server_dao.get_all_users()]
    return jsonify({'users': users})


@app.route(BASE_URI + '/<user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    app.logger.info('Getting user %d', user_id)
    user = rest_server_dao.get_user(user_id)
    if user is None:
        abort(404)
    return jsonify({'user': make_public_user(user)})


@app.route(BASE_URI, methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or 'title' not in request.json:
        abort(400)
    title = request.json['title']
    desc = request.json.get('description', '')
    done = False
    app.logger.info('Creating user "%s", "%s", %d', title, desc, done)
    user = rest_server_dao.create_user(title, desc, done)
    return jsonify({'user': make_public_user(user)}), 201  # 201 == Created


@app.route(BASE_URI + '/<user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    if 'description' in request.json \
            and not isinstance(request.json['description'], str):
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    title = request.json.get('title')
    desc = request.json.get('description')
    done = request.json.get('done')
    app.logger.info('Updating user %d (s" "%s" %s)',
                    user_id, title, desc, '' if done is None else str(done))
    user = rest_server_dao.update_user(user_id, title, desc, done)
    if user is None:
        abort(404)
    return jsonify({'user': make_public_user(user)}), 202  # 202 == Accepted


@app.route(BASE_URI + '/<user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    app.logger.info('Deleting user %d', user_id)
    if not rest_server_dao.delete_user(user_id):
        abort(404)
    return Response(status=204)  # 204 == No Content


if __name__ == '__main__':
    app.run(debug=True)  # debug=True activates HTML debug messages
