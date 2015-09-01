"""
rest_server_json.py - Example from
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""

from flask import (Flask, jsonify, abort, request, make_response, url_for,
                   Response)
from flask.ext.httpauth import HTTPBasicAuth  # ignore PyCharm error
# pip install Flask-HTTPAuth

import rest_server_dao


__author__ = 'Miguel Grinberg (https://www.linkedin.com/in/miguelgrinberg)'

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


BASE_URI = '/todo/api/v1.0/tasks'


@app.route(BASE_URI, methods=['GET'])
@auth.login_required
def get_tasks():
    app.logger.info('Getting all tasks')
    tasks = rest_server_dao.get_all_tasks()
    return jsonify({'tasks': tasks})


@app.route(BASE_URI + '/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    app.logger.info('Getting task %d', task_id)
    task = rest_server_dao.get_task(task_id)
    if task is None:
        abort(404)
    return jsonify({'task': task})


@app.route(BASE_URI, methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    title = request.json['title']
    desc = request.json.get('description', '')
    done = False
    app.logger.info('Creating task "%s", "%s", %d', title, desc, done)
    task = rest_server_dao.create_task(title, desc, done)
    return jsonify({'task': task}), 201  # 201 == Created


@app.route(BASE_URI + '/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
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
    app.logger.info('Updating task %d (s" "%s" %s)',
                    task_id, title, desc, '' if done is None else str(done))
    task = rest_server_dao.update_task(task_id, title, desc, done)
    if task is None:
        abort(404)
    return jsonify({'task': task}), 202  # 202 == Accepted


@app.route(BASE_URI + '/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    app.logger.info('Deleting task %d', task_id)
    if not rest_server_dao.delete_task(task_id):
        abort(404)
    return Response(status=204)  # 204 == No Content


def make_public_task(task):
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
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True)  # debug=True activates HTML debug messages
