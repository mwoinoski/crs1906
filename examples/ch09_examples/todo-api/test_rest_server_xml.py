"""
test_rest_server_xml.py - Unit tests for rest_server_xml.py
"""
import unittest
from xml.etree import ElementTree

import rest_server_xml


class TestRestServer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def test_xmlify_element(self):
        expected = '<error>Unauthorized access</error>'

        xml = rest_server_xml.xmlify_element('error', 'Unauthorized access')

        self.assertEqual(expected, xml)

    def test_xmlify_task_all_members(self):
        task = {
            'id': 1,
            'title': 'Task title',
            'description': 'Task description',
            'done': False,
            'uri': 'http://localhost/todo'
        }
        expected = '<task>' +\
                       '<id>1</id>' +\
                       '<title>Task title</title>' +\
                       '<description>Task description</description>' +\
                       '<done>False</done>' +\
                       '<uri>http://localhost/todo</uri>' +\
                   '</task>'

        xml = rest_server_xml.xmlify_task(task)

        self.assertEqual(expected, xml)

    def test_xmlify_task_missing_members(self):
        task = {
            'title': 'Task title',
            'description': 'Task description',
            'done': False,
        }
        expected = '<task>' +\
                       '<title>Task title</title>' +\
                       '<description>Task description</description>' +\
                       '<done>False</done>' +\
                   '</task>'

        xml = rest_server_xml.xmlify_task(task)

        self.assertEqual(expected, xml)

    def test_xmlify_list(self):
        tasks = [
            {
            'id': 1,
            'title': 'Task title',
            'description': 'Task description',
            'done': False,
            'uri': 'http://localhost/todo'
            },
            {
            'id': 2,
            'title': 'Task title 2',
            'description': 'Task description 2',
            'done': True
            },
        ]
        expected = '<tasks>' +\
                       '<task>' +\
                           '<id>1</id>' +\
                           '<title>Task title</title>' +\
                           '<description>Task description</description>' +\
                           '<done>False</done>' +\
                           '<uri>http://localhost/todo</uri>' +\
                       '</task>' +\
                       '<task>' +\
                           '<id>2</id>' +\
                           '<title>Task title 2</title>' +\
                           '<description>Task description 2</description>' +\
                           '<done>True</done>' +\
                       '</task>' +\
                   '</tasks>'

        xml = rest_server_xml.xmlify_list(tasks)

        self.assertEqual(expected, xml)

    def test_parse_task_xml(self):
        xml = '<task><title>Task title</title>' +\
              '<description>Task description</description>' +\
              '<done>False</done></task>'

        title, desc, done = rest_server_xml.parse_task_xml(xml)

        self.assertEqual('Task title', title)
        self.assertEqual('Task description', desc)
        self.assertEqual(False, done)


    def test_parse_task_xml_no_elements(self):
        xml = '<task></task>'

        title, desc, done = rest_server_xml.parse_task_xml(xml)

        self.assertEqual(None, title)
        self.assertEqual(None, desc)
        self.assertEqual(None, done)


if __name__ == '__main__':
    unittest.main()
