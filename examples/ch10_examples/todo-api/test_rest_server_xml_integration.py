"""
test_rest_server_xml.py - Integration tests for rest_server_xml.py
"""
import unittest
from xml.etree import ElementTree
import requests


class TestRestServer(unittest.TestCase):
    base_url = 'http://localhost:5000/todo/api/v1.0/tasks'

    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def parse_task_xml(self, xml_str):
        root = ElementTree.fromstring(xml_str)
        title = root.findtext('./title')
        desc = root.findtext('./description')
        uri = root.findtext('./uri')
        done = root.findtext('./done')
        return title, desc, done, uri

    def parse_tasks_xml(self, xml_str):
        tasks = []
        tasks_element = ElementTree.fromstring(xml_str)
        for task_element in tasks_element:  # iterate over children of <tasks>
            title = task_element.findtext('./title')
            desc = task_element.findtext('./description')
            uri = task_element.findtext('./uri')
            done = task_element.findtext('./done')
            tasks.append((title, desc, done, uri))
        return tasks

    def create_task_xml(self, task):
        task_element = ElementTree.Element('task')
        for field in ('title', 'description', 'done', 'uri'):
            if task.get(field) is not None:
                element = ElementTree.SubElement(task_element, field)
                element.text = str(task[field])
        return ElementTree.tostring(task_element, encoding='unicode')

    def test_01_get_all_tasks(self):
        http_hdrs = {'Content-Type': 'application/xml'}
        creds = ('student', 'studentpw')

        r = requests.get(TestRestServer.base_url, auth=creds, headers=http_hdrs)

        tasks = self.parse_tasks_xml(r.text)

        self.assertEqual('Teach cat Spanish', tasks[0][0])
        self.assertEqual('Needs to work on irregular verbs', tasks[0][1])
        self.assertEqual('False', tasks[0][2])
        self.assertEqual('http://localhost:5000/todo/api/v1.0/tasks/1', tasks[0][3])
        self.assertEqual('Untangle Gordian knot', tasks[1][0])
        self.assertEqual('Remember what happened last time', tasks[1][1])
        self.assertEqual('False', tasks[1][2])
        self.assertEqual('http://localhost:5000/todo/api/v1.0/tasks/2', tasks[1][3])
        self.assertEqual(200, r.status_code)

    def test_02_post_task(self):
        title = 'Get jetpack serviced'
        desc = 'Thruster response is sluggish'
        done = 'False'
        uri = 'http://localhost:5000/todo/api/v1.0/tasks/3'
        task = {
            'title': title,
            'description': desc,
            'done': done,
        }
        xml_data = self.create_task_xml(task)

        url = TestRestServer.base_url
        http_hdrs = {'Content-Type': 'application/xml'}
        creds = ('student', 'studentpw')

        r = requests.post(url, auth=creds, headers=http_hdrs, data=xml_data)

        res_title, res_desc, res_done, res_uri = self.parse_task_xml(r.text)

        self.assertEqual(title, res_title)
        self.assertEqual(desc, res_desc)
        self.assertEqual(done, res_done)
        self.assertEqual(uri, res_uri)
        self.assertEqual(201, r.status_code)

    def test_03_get_task(self):
        url = '{}/{}'.format(TestRestServer.base_url, 3)
        http_hdrs = {'Content-Type': 'application/xml'}
        creds = ('student', 'studentpw')

        r = requests.get(url, auth=creds, headers=http_hdrs)

        res_title, res_desc, res_done, res_uri = self.parse_task_xml(r.text)

        self.assertEqual('Get jetpack serviced', res_title)
        self.assertEqual('Thruster response is sluggish', res_desc)
        self.assertEqual('False', res_done)
        self.assertEqual('http://localhost:5000/todo/api/v1.0/tasks/3', res_uri)
        self.assertEqual(200, r.status_code)

    def test_04_put_task(self):
        title = 'Get jetpack serviced'
        desc = 'Thruster response is sluggish'
        done = 'True'
        uri = 'http://localhost:5000/todo/api/v1.0/tasks/3'
        task = {'done': done}
        xml_data = self.create_task_xml(task)

        url = '{}/{}'.format(TestRestServer.base_url, 3)
        http_hdrs = {'Content-Type': 'application/xml'}
        creds = ('student', 'studentpw')

        r = requests.put(url, auth=creds, headers=http_hdrs, data=xml_data)

        res_title, res_desc, res_done, res_uri = self.parse_task_xml(r.text)

        self.assertEqual(title, res_title)
        self.assertEqual(desc, res_desc)
        self.assertEqual(done, res_done)
        self.assertEqual(uri, res_uri)
        self.assertEqual(202, r.status_code)

    def test_05_create_task_simple(self):
        task = ElementTree.Element('task')
        child = ElementTree.SubElement(task, 'title')
        child.text = 'Get jetpack serviced'
        child = ElementTree.SubElement(task, 'description')
        child.text = 'Thruster response is sluggish'
        child = ElementTree.SubElement(task, 'done')
        child.text = 'False'
        xml_data = ElementTree.tostring(task)

        url = TestRestServer.base_url
        http_hdrs = {'Content-Type': 'application/xml'}
        creds = ('student', 'studentpw')

        r = requests.post(url, auth=creds, headers=http_hdrs, data=xml_data)

        title, desc, done, uri = self.parse_task_xml(r.text)

        self.assertEqual('Get jetpack serviced', title)
        self.assertEqual('Thruster response is sluggish', desc)
        self.assertEqual('False', done)
        self.assertEqual('http://localhost:5000/todo/api/v1.0/tasks/4', uri)
        self.assertEqual(201, r.status_code)

    def test_06_delete_task(self):
        url = '{}/{}'.format(TestRestServer.base_url, 3)
        creds = ('student', 'studentpw')
        r = requests.delete(url, auth=creds)
        self.assertEqual(204, r.status_code)

        url = '{}/{}'.format(TestRestServer.base_url, 4)
        creds = ('student', 'studentpw')
        r = requests.delete(url, auth=creds)
        self.assertEqual(204, r.status_code)

    def test_99_get_task_bad_creds(self):
        expected = '<error>Unauthorized access</error>'
        url = '{}/{}'.format(TestRestServer.base_url, 1)
        http_hdrs = {'Content-Type': 'application/xml'}
        creds = ('homer', 'donuts')

        r = requests.get(url, auth=creds, headers=http_hdrs)

        self.assertEqual(expected, r.text)

if __name__ == '__main__':
    unittest.main(failfast=True)

# r = requests.post(url, data=json.dumps(payload))
