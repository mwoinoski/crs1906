"""
test_rest_server_json.py - Integration tests for rest_server_json.py
"""
import json
import unittest
import requests


class TestRestServer(unittest.TestCase):
    base_url = 'http://localhost:5000/todo/api/v1.0/tasks'

    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def test_01_get_all_tasks(self):
        tasks = [
            {'title': 'Teach cat Spanish',
             'description': 'Needs to work on irregular verbs',
             'done': False,
             'uri': 'http://localhost:5000/todo/api/v1.0/tasks/1'},
            {'title': 'Untangle Gordian knot',
             'description': 'Remember what happened last time',
             'done': False,
             'uri': 'http://localhost:5000/todo/api/v1.0/tasks/2'}
        ]
        http_hdrs = {'Content-Type': 'application/json'}
        creds = ('student', 'studentpw')

        r = requests.get(TestRestServer.base_url, auth=creds, headers=http_hdrs)
        json_dict = r.json()

        self.assertEqual({'tasks': tasks}, json_dict)
        self.assertEqual(200, r.status_code)

    def test_02_post_task(self):
        task = {
            'title': 'Get jetpack serviced',
            'description': 'Thruster response is sluggish',
            'done': False,
        }
        json_data = json.dumps(task)

        task['uri'] = 'http://localhost:5000/todo/api/v1.0/tasks/3'

        url = TestRestServer.base_url
        http_hdrs = {'Content-Type': 'application/json'}
        creds = ('student', 'studentpw')

        r = requests.post(url, auth=creds, headers=http_hdrs, data=json_data)
        json_dict = r.json()

        self.assertEqual({'task': task}, json_dict)
        self.assertEqual(201, r.status_code)

    def test_03_get_task(self):
        url = '{}/{}'.format(TestRestServer.base_url, 3)
        http_hdrs = {'Content-Type': 'application/json'}
        creds = ('student', 'studentpw')
        task = {
            'title': 'Get jetpack serviced',
            'description': 'Thruster response is sluggish',
            'done': False,
            'uri': 'http://localhost:5000/todo/api/v1.0/tasks/3',
        }

        r = requests.get(url, auth=creds, headers=http_hdrs)
        json_dict = r.json()

        self.assertEqual({'task': task}, json_dict)
        self.assertEqual(200, r.status_code)

    def test_04_put_task(self):
        expected = {
            'title': 'Get jetpack serviced',
            'description': 'Thruster response is sluggish',
            'done': True,
            'uri': 'http://localhost:5000/todo/api/v1.0/tasks/3',
        }
        task = {'done': True}
        json_data = json.dumps(task)

        url = '{}/{}'.format(TestRestServer.base_url, 3)
        http_hdrs = {'Content-Type': 'application/json'}
        creds = ('student', 'studentpw')

        r = requests.put(url, auth=creds, headers=http_hdrs, data=json_data)
        json_dict = r.json()

        self.assertEqual({'task': expected}, json_dict)
        self.assertEqual(202, r.status_code)

    def test_06_delete_task(self):
        url = '{}/{}'.format(TestRestServer.base_url, 3)
        creds = ('student', 'studentpw')
        r = requests.delete(url, auth=creds)
        self.assertEqual(204, r.status_code)

    def test_99_get_task_bad_creds(self):
        expected = {'error': 'Unauthorized access'}
        url = '{}/{}'.format(TestRestServer.base_url, 1)
        http_hdrs = {'Content-Type': 'application/json'}
        creds = ('homer', 'donuts')

        r = requests.get(url, auth=creds, headers=http_hdrs)
        json_dict = r.json()

        self.assertEqual(expected, json_dict)

if __name__ == '__main__':
    unittest.main(failfast=True)
