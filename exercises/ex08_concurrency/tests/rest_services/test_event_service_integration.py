"""
Integration tests for EventServiceRest.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import json

import unittest
from webtest import TestApp
from ticketmanor import main
from tests.test_support.db_utils import (
    create_db_tables,
    drop_db_tables,
    execute_select,
    execute_insert,
)

# SQLAlchemy can't connect to an in-memory SQLite database, so we'll
# use a temporary database file.

db_filename = 'test_db.sqlite'


class EventServiceRestIntegrationTest(unittest.TestCase):
    """
    Integration tests for EventServiceRest
    """

    def setUp(self):
        create_db_tables(db_filename)
        self.populate_db_tables()

        settings = {'sqlalchemy.url': 'sqlite:///' + db_filename}
        app = main(None, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        drop_db_tables(db_filename)

    def test_get_events_for_act_found(self):
        url = 'http://localhost:6543/rest/events/music.json?' \
              'event_type=Artist&words=Berlin+Philharmonic&page=0&page_size=6'
        headers = {'Accept': 'application/json; charset=utf8'}
        expected_res = {
            'id': 301,
            'act_type': 'music',
            'title': 'Berlin Philharmonic',
            'notes': 'Beethoven and Brahms',
            'page': 0,
            'page_size': 6,
            'year': 0,
            'events': [
                {
                    'id': 204,
                    'venue': {
                        'latitude': 40.7127,
                        'prov_state': 'NY',
                        'longitude': -74.0059,
                        'name': 'Carnegie Hall',
                        'country': 'USA',
                        'id': 102,
                        'street_address': '881 7th Ave, New York, NY 10019',
                        'city': 'New York'
                    },
                    # 'price': '$180'  # FIXME: uncomment when database schema is complete
                    # 'image_thumbnail': '/static/images/concerts-1.png',
                    # 'image_banner': '/static/images/concerts.jpg',
                },
                {
                    'id': 201,
                    'venue': {
                        'latitude': 41.8369,
                        'prov_state': 'IL',
                        'longitude': -87.6847,
                        'name': 'Auditorium Theatre',
                        'country': 'USA',
                        'id': 101,
                        'street_address': 'E Congress Pkwy, Chicago, IL 60605',
                        'city': 'Chicago'
                    },
                    # 'price': '$160'
                    # 'image_thumbnail': '/static/images/concerts-2.png',
                    # 'image_banner': '/static/images/concerts.jpg',
                },
                {
                    'id': 203,
                    'venue': {
                        'latitude': 40.7127,
                        'prov_state': 'NY',
                        'longitude': -74.0059,
                        'name': 'Carnegie Hall',
                        'country': 'USA',
                        'id': 102,
                        'street_address': '881 7th Ave, New York, NY 10019',
                        'city': 'New York'
                    },
                    # 'price': '$225'
                    # 'image_thumbnail': '/static/images/concerts-3.png',
                    # 'image_banner': '/static/images/concerts.jpg',
                },
                {
                    'id': 202,
                    'venue': {
                        'latitude': 41.8369,
                        'prov_state': 'IL',
                        'longitude': -87.6847,
                        'name': 'Auditorium Theatre',
                        'country': 'USA',
                        'id': 101,
                        'street_address': 'E Congress Pkwy, Chicago, IL 60605',
                        'city': 'Chicago'
                    },
                    # 'price': '$175'
                    # 'image_thumbnail': '/static/images/concerts-4.png',
                    # 'image_banner': '/static/images/concerts.jpg',
                },
            ]
        }

        res = self.testapp.get(url, headers=headers, status=200)

        res_list = json.loads(str(res.body, 'utf-8'))
        for e in res_list['events']:  # FIXME: delete when database schema is complete
            del e['price']
            del e['image_thumbnail']
            del e['image_banner']
            del e['date_time']
        self.maxDiff = None
        self.assertEqual(expected_res, res_list)

    def test_get_events_for_act_not_found(self):
        url = 'http://localhost:6543/rest/events/music.json?' \
              'event_type=Artist&words=Never+Heard+Of+Them&page=0&page_size=6'
        headers = {'Accept': 'application/json; charset=utf8'}

        res = self.testapp.get(url, headers=headers, status=200)

        res_dict = json.loads(str(res.body, 'utf-8'))
        self.assertFalse(res_dict)

    # def test_search_for_events_by_venue(self):
    #     url = 'http://localhost:6543/rest/events/music/search?venue=Carnegie+Hall'
    #     headers = {'Accept': 'application/json; charset=utf8'}
    #     expected_res = [
    #         {'act_id': 301, 'act_title': 'Berlin Philharmonic', 'act_type': 'music',
    #          'event_id': 204, 'date_time': '2015-12-25 10:00:00',
    #          'venue_name': 'Carnegie Hall', 'venue_city': 'New York',
    #          'venue_prov_st': 'NY', 'venue_country': 'USA'},
    #         {'act_id': 301, 'act_title': 'Berlin Philharmonic', 'act_type': 'music',
    #          'event_id': 203, 'date_time': '2015-12-31 21:00:00',
    #          'venue_name': 'Carnegie Hall', 'venue_city': 'New York',
    #          'venue_prov_st': 'NY', 'venue_country': 'USA'},
    #         {'act_id': 305, 'act_title': 'Take 6', 'act_type': 'music',
    #          'event_id': 205, 'date_time': '2016-01-01 10:00:00',
    #          'venue_name': 'Carnegie Hall', 'venue_city': 'New York',
    #          'venue_prov_st': 'NY', 'venue_country': 'USA'},
    #     ]
    #
    #     res = self.testapp.get(url, headers=headers, status=200)
    #
    #     res_list = json.loads(str(res.body, 'utf-8'))
    #     self.maxDiff = None
    #     self.assertEqual(expected_res, res_list)

    def populate_db_tables(self):
        execute_insert(db_filename, 'acts',
            (301, 'Beethoven and Brahms', 'Berlin Philharmonic', 1, 0),
            (302, 'Unplugged', 'Eric Clapton', 1, 0),
            (303, 'Gershwin Rhapsody in Blue', 'New York Philharmonic', 1, 0),
            (304, 'Sketches of Spain', 'Wynton Marsalis', 1, 0),
            (305, 'The Standard', 'Take 6', 1, 0)
        )
        execute_insert(db_filename, 'acts_events',
            (301, 201),
            (301, 202),
            (301, 203),
            (301, 204),
            (302, 201),
            (302, 202),
            (303, 201),
            (304, 201),
            (305, 205)
        )
        execute_insert(db_filename, 'events',
            (201, '2015-12-31 20:00:00.000', 101, None),
            (202, '2016-01-01 20:00:00.000', 101, None),
            (203, '2015-12-31 21:00:00.000', 102, None),
            (204, '2015-12-25 10:00:00.000', 102, None),
            (205, '2016-01-01 10:00:00.000', 102, None),
        )
        execute_insert(db_filename, 'venues',
            (101, 'Chicago', 'USA', 41.8369, -87.6847, 'Auditorium Theatre',
             'IL', 'E Congress Pkwy, Chicago, IL 60605'),
            (102, 'New York', 'USA', 40.7127, -74.0059, 'Carnegie Hall',
             'NY', '881 7th Ave, New York, NY 10019')
        )

if __name__ == '__main__':
    unittest.main()
