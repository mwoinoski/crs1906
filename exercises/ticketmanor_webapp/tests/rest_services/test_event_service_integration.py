"""
Integration tests for EventServiceRest.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import os
import json

from unittest import TestCase
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


class EventServiceRestIntegrationTest(TestCase):
    """
    Integration tests for EventServiceRest
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

    def test_get_events_for_act_found(self):
        url = 'http://localhost:6543/rest/events/music?title=London+Symphony&page=1&page_size=6'
        headers = {'Accept': 'application/json; charset=utf8'}
        expected_res = [
            {'act_id': 301,
             'act_title': 'Berlin Philharmonic',
             'act_type': 'music',
             'title': 'Beethoven and Brahms',
             'image_thumbnail': '/static/images/concerts-1.png',
             'image_banner': '/static/images/Lorem-ipsum-portland-marketing.jpg',
             'date_time': '2015-12-25 10:00:00',
             'venue_country': 'USA',
             'venue_name': 'Carnegie Hall',
             'event_id': 204,
             'venue_city': 'New York',
             'venue_prov_st': 'NY',
             # 'price': '$180'  # TODO: replace when database is fixed
             },
            {'act_id': 301,
             'act_title': 'Berlin Philharmonic',
             'act_type': 'music',
             'title': 'Beethoven and Brahms',
             'image_thumbnail': '/static/images/concerts-1.png',
             'image_banner': '/static/images/Lorem-ipsum-portland-marketing.jpg',
             'date_time': '2015-12-31 20:00:00',
             'venue_country': 'USA',
             'venue_name': 'Auditorium Theatre',
             'event_id': 201,
             'venue_city': 'Chicago',
             'venue_prov_st': 'IL',
             # 'price': '$160'
             },
            {'act_id': 301,
             'act_title': 'Berlin Philharmonic',
             'act_type': 'music',
             'title': 'Beethoven and Brahms',
             'image_thumbnail': '/static/images/concerts-1.png',
             'image_banner': '/static/images/Lorem-ipsum-portland-marketing.jpg',
             'date_time': '2015-12-31 21:00:00',
             'venue_country': 'USA',
             'venue_name': 'Carnegie Hall',
             'event_id': 203,
             'venue_city': 'New York',
             'venue_prov_st': 'NY',
             # 'price': '$225'
             },
            {'act_id': 301,
             'act_title': 'Berlin Philharmonic',
             'act_type': 'music',
             'title': 'Beethoven and Brahms',
             'image_thumbnail': '/static/images/concerts-1.png',
             'image_banner': '/static/images/Lorem-ipsum-portland-marketing.jpg',
             'date_time': '2016-01-01 20:00:00',
             'venue_country': 'USA',
             'venue_name': 'Auditorium Theatre',
             'event_id': 202,
             'venue_city': 'Chicago',
             'venue_prov_st': 'IL',
             # 'price': '$175'
             },
        ]

        res = self.testapp.get(url, headers=headers, status=200)

        res_list = json.loads(str(res.body, 'utf-8'))
        for e in res_list:  # TODO: delete when database is fixed
            del e['price']
        self.maxDiff = None
        self.assertEqual(expected_res, res_list)

    def test_get_events_for_act_not_found(self):
        url = 'http://localhost:6543/rest/events/music?title=Never+Heard+Of+Them'
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
