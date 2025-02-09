"""
rest-server_xml.py - Based on an example from
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""

from flask import Flask, abort, request, make_response, url_for, Response
from flask_httpauth import HTTPBasicAuth
from xml.dom.minidom import getDOMImplementation
import xml.etree.ElementTree as ElementTree

import rest_server_dao

__author__ = 'Miguel Grinberg (https://www.linkedin.com/in/miguelgrinberg)'

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    """Callback function that returns the password for username"""
    return rest_server_dao.get_password(username)


@auth.error_handler
def unauthorized():
    return make_response(xmlify_element('error', 'Unauthorized access'), 401)
    # Note: if the client is a browser, the 401 would cause a browser to
    # display the default auth dialog. But that shouldn't be a problem here
    # because the request will ben an asynchronous call from a JavaScript or
    # a Python client.
    

@app.errorhandler(400)
def not_found400(error):
    return make_response(xmlify_element('error', 'Bad request'), 400)


@app.errorhandler(404)
def not_found404(error):
    return make_response(xmlify_element('error', 'Not found'), 404)


def make_public_task(task):
    """Add a uri attribute to a task.

    The client uses the task's uri to perform operations on the task by
    accessing the uri with HTTP GET, PUT, or DELETE."""
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


BASE_URI = '/todo/api/v1.0/tasks'


@app.route(BASE_URI, methods=['GET'])
@auth.login_required
def get_tasks():
    app.logger.info('Getting all tasks')
    tasks = [make_public_task(task)
             for task in rest_server_dao.get_all_tasks()]
    return xmlify_list(tasks)


@app.route(BASE_URI + '/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    app.logger.info('Getting task %d', task_id)
    task = rest_server_dao.get_task(task_id)
    if task is None:
        abort(404)
    return xmlify_task(make_public_task(task))


def xmlify_task(task):
    """Return a string with the task marshalled as XML"""
    return ElementTree.tostring(create_xml_element(task), encoding='unicode')


def create_xml_element(task):
    """Return ElementTree.Element that represents the given task.

    Missing attributes in task do not generate Elements."""
    task_element = ElementTree.Element('task')
    for field in ('id', 'title', 'description', 'done', 'uri'):
        if task.get(field) is not None:
            element = ElementTree.SubElement(task_element, field)
            element.text = str(task[field])
    return task_element


def xmlify_list(tasks):
    """Return a string with the list of tasks marshalled as XML"""
    tasks_element = ElementTree.Element('tasks')
    for task in tasks:
        tasks_element.append(create_xml_element(task))
    return ElementTree.tostring(tasks_element, encoding='unicode')


def xmlify_element(name, value):
    """Return a string with a single XML element

    :param name the XML element name
    :param value the text content of the element"""
    element = ElementTree.Element(name)
    element.text = value if value is not None else ''
    return ElementTree.tostring(element, encoding='unicode')


@app.route(BASE_URI, methods=['POST'])
@auth.login_required
def create_task():
    if not request.data:
        abort(400)
    title, desc, done = parse_task_xml(request.data)
    if title is None:
        abort(400)
    if done is None:
        done = False
    if desc is None:
        desc = ''
    app.logger.info('Creating task "%s", "%s", %d', title, desc, done)
    task = rest_server_dao.create_task(title, desc, done)
    return xmlify_task(make_public_task(task)), 201  # 201 == Created


def parse_task_xml(xml_str):
    """Parses the XML for elements <title>, <description>, and <done>.

    If an element is missing, the value returned is None.
    If an element is present but has empty content, the value returned is
    an empty string"""
    task = ElementTree.fromstring(xml_str)
    title = task.findtext('./title')
    desc = task.findtext('./description')
    done = task.findtext('./done')
    # if done is None, just return it
    if done:
        done = (done == 'True')
    return title, desc, done


@app.route(BASE_URI + '/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    if not request.data:
        abort(400)
    title, desc, done = parse_task_xml(request.data)
    is_valid(title, desc, done)
    app.logger.info('Updating task %d ("%s" "%s" %s)',
                    task_id, title, desc, '' if done is None else str(done))
    task = rest_server_dao.update_task(task_id, title, desc, done)
    if task is None:
        abort(404)
    return xmlify_task(make_public_task(task)), 202  # 202 == Accepted


def is_valid(title, desc, done):
    if title is not None and not isinstance(title, str):
        abort(400)
    if desc is not None and not isinstance(desc, str):
        abort(400)
    if done is not None and not isinstance(done, bool):
        abort(400)


@app.route(BASE_URI + '/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    app.logger.info('Deleting task %d', task_id)
    if not rest_server_dao.delete_task(task_id):
        abort(404)
    return Response(status=204)  # 204 == No Content


if __name__ == '__main__':
    app.run(debug=True)  # debug=True activates HTML debug messages
