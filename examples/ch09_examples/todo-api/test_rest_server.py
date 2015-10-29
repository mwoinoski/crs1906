"""
test_rest_server.py - Integration tests for rest_server_json.py
"""

import unittest
import requests

base_url = 'http://localhost:5000/todo/api/v1.0/tasks'


def get_task(task_id):
    http_hdrs = {'Accept': 'application/json'}
    creds = ('student', 'studentpw')
    url = '{}/{}'.format(base_url, task_id)

    r = requests.get(url, auth=creds, headers=http_hdrs)

    if r.status_code != 200:
        raise RuntimeError('Oops')

    json_result = r.json()

    task = json_result['task']
    return task['title'], task['description'], task['done']


def create_task(title, description, done):
    http_hdrs = {'Content-Type': 'application/json'}
    creds = ('student', 'studentpw')
    task = {
        'title': title,
        'description': description,
        'done': done,
    }

    r = requests.post(base_url, auth=creds, headers=http_hdrs,
                      json=task)

    if r.status_code != 201:
        raise RuntimeError('Problem creating task')

    return r.json()


def update_task(id, task):
    url = '{}/{}'.format(base_url, id)
    http_hdrs = {'Accept': 'application/json'}
    creds = ('student', 'studentpw')

    r = requests.put(url, auth=creds,
                     headers=http_hdrs, json=task)

    if r.status_code != 202:
        raise RuntimeError('Problem updating task')

    return r.json()


def delete_task(id):
    url = '{}/{}'.format(base_url, id)

    r = requests.delete(url, auth=('student', 'studentpw'))

    if r.status_code != 204:
        raise RuntimeError('Problem deleting task')


class TestRestServer(unittest.TestCase):
    new_task_id = None

    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def test_01_get_all_tasks(self):
        tasks = [
            {'title': 'Teach cat Spanish',
             'description': 'Needs to work on irregular verbs',
             'done': False},
            {'title': 'Untangle Gordian knot',
             'description': 'Remember what happened last time',
             'done': False}
        ]
        http_hdrs = {'Accept': 'application/json'}
        creds = ('student', 'studentpw')

        r = requests.get(base_url, auth=creds,
                         headers=http_hdrs)
        json_dict = r.json()

        self.assertEqual(200, r.status_code)
        for task in json_dict['tasks']:
            del task['id']
        self.assertEqual(tasks, json_dict['tasks'][:2])

    def test_02_post_task(self):
        expected_title = 'Get jetpack serviced'
        expected_description = 'Thruster response is sluggish'
        expected_done = False
        task = {
            'title': expected_title,
            'description': expected_description,
            'done': expected_done,
        }

        json_dict = create_task(expected_title, expected_description,
                                expected_done)

        TestRestServer.new_task_id = json_dict['task'].pop('id')
        self.assertEqual({'task': task}, json_dict)

    def test_03_get_task(self):
        expected_title = 'Get jetpack serviced'
        expected_description = 'Thruster response is sluggish'
        expected_done = False

        title, description, done = get_task(TestRestServer.new_task_id)

        self.assertEqual(expected_title, title)
        self.assertEqual(expected_description, description)
        self.assertEqual(expected_done, done)

    def test_04_put_task(self):
        expected = {
            'id': TestRestServer.new_task_id,
            'title': 'Get jetpack serviced',
            'description': 'Thruster response is sluggish',
            'done': True,
        }
        task = {'done': True}

        json_dict = update_task(TestRestServer.new_task_id, task)

        self.assertEqual({'task': expected}, json_dict)

    def test_06_delete_task(self):
        delete_task(TestRestServer.new_task_id)

    def test_99_get_task_bad_creds(self):
        expected = {'error': 'Unauthorized access'}
        url = '{}/{}'.format(base_url,
                             TestRestServer.new_task_id)
        http_hdrs = {'Accept': 'application/json'}
        creds = ('homer', 'donuts')

        r = requests.get(url, auth=creds, headers=http_hdrs)
        json_dict = r.json()

        self.assertEqual(expected, json_dict)

if __name__ == '__main__':
    unittest.main(failfast=True)
