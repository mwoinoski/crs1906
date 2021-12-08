"""
Integration tests for UserServiceRest.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import os
import json

import unittest
from webtest import TestApp
from ticketmanor import main
from test_support.db_utils import (
    create_db_tables,
    drop_db_tables,
    execute_select,
    execute_insert,
)

# SQLAlchemy can't connect to an in-memory SQLite database, so we'll
# use a temporary database file.

db_filename = 'ticketmanor_db.sqlite'


class UserServiceRestIntegrationTest(unittest.TestCase):
    """
    Integration tests for UserServiceRest
    """

    @classmethod
    def tearDownClass(cls):
        os.remove(db_filename)

    def setUp(self):
        create_db_tables(db_filename)
        self.populate_db_tables()

        settings = {'sqlalchemy.url': 'sqlite:///' + db_filename}
        app = main(None, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        drop_db_tables(db_filename)

    def test_get_user_found(self):
        url = 'http://localhost:6543/rest/users/trane@jazz.com'
        headers = {'Accept': 'application/json; charset=utf8'}

        res = self.testapp.get(url, headers=headers, status=200)

        res_dict = json.loads(str(res.body, 'utf-8'))
        self.assertEqual('trane@jazz.com', res_dict['email'])
        self.assertEqual('Coltrane', res_dict['last_name'])
        self.assertEqual('34568', res_dict['address']['post_code'])

    def test_get_user_not_found(self):
        url = 'http://localhost:6543/rest/users/nobody@nowhere.com'
        headers = {'Accept': 'application/json; charset=utf8'}

        res = self.testapp.get(url, headers=headers, status=404)

    def test_add_user_ok(self):
        url = 'http://localhost:6543/rest/users'
        post_body = {
            "email": "miles@jazz.com",
            "middles": None,
            "address": {
                "country": "USA",
                "street": "5311 E 1st St",
                "city": "New York",
                "post_code": "10012",
                "state": "NY"
            },
            "first_name": "Miles",
            "last_name": "Davis"
        }

        res = self.testapp.post_json(url, post_body, status=201)

        rows = execute_select(db_filename,
            "select * from people where email = 'miles@jazz.com'")
        self.assertEqual("Miles", rows[0][7])

    def test_update_user_ok(self):
        url = 'http://localhost:6543/rest/users'
        put_body = {
            "id": 123,  # id must be set for update
            "email": "trane@jazz.com",
            "middles": "William",
            "address": {
                "country": "USA",
                "street": "123 Cool St",
                "city": "Chicago",
                "post_code": "34568",
                "state": "IL"
            },
            "first_name": "John",
            "last_name": "Coltrance"
        }

        res = self.testapp.put_json(url, put_body, status=202)

        rows = execute_select(db_filename,
            "select * from people where email = 'trane@jazz.com'")
        self.assertEqual("John", rows[0][7])
        self.assertEqual("William", rows[0][9])

    def test_delete_user_found(self):
        url = 'http://localhost:6543/rest/users/trane@jazz.com'

        self.testapp.delete(url, status=204)

    def test_delete_user_not_found(self):
        url = 'http://localhost:6543/rest/users/nobody@nowhere.com'

        res = self.testapp.delete(url, status=404)

    def populate_db_tables(self):
        execute_insert(db_filename, 'people',
            (123, 'Chicago', 'USA', '34568', 'IL', '123 Cool St',
             'trane@jazz.com', 'John', 'Coltrane', ''),
            (124, 'New Paltz', 'USA', '12345', 'NY', '123 Main St',
                'mike@jazz.com', 'Mike', 'Woinoski', '')
        )

if __name__ == '__main__':
    unittest.main()
