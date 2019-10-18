"""
Integration tests for ActDao.
"""
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import os
from sqlalchemy.orm import sessionmaker

from unittest import TestCase
from ticketmanor import engine_from_config
from test_support.db_utils import (
    create_db_tables,
    drop_db_tables,
    execute_select,
    execute_insert,
)
from ticketmanor.models.act import Act
from ticketmanor.models.persistence.act_dao import ActDao

# The following imports for Event and Venue are required.
# Without them, SQLAlchemy raises exceptions.
from ticketmanor.models.event import Event
from ticketmanor.models.venue import Venue

# SQLAlchemy can't connect to an in-memory SQLite database, so we'll
# use a temporary database file.

db_filename = 'ticketmanor_db.sqlite'


class ActDaoTest(TestCase):
    """
    Integration tests for ActDao
    """

    # -------------------------------------------------------------------------
    #                              Test Cases
    # -------------------------------------------------------------------------

    def test_get_act_found(self):

        act = self.act_dao.get(301, self.session)

        self.assertEqual(301, act.id)
        self.assertEqual('Berlin Philharmonic', act.title)
        self.assertEqual('Beethoven and Brahms', act.notes)
        self.assertEqual(1, act.act_type)
        self.assertEqual(4, len(act.events))
        # An Act's Events are sorted by their date_time
        self.assertEqual(204, act.events[0].id)
        self.assertEqual(102, act.events[0].venue.id)
        self.assertEqual(201, act.events[1].id)
        self.assertEqual(101, act.events[1].venue.id)
        self.assertEqual(203, act.events[2].id)
        self.assertEqual(102, act.events[2].venue.id)
        self.assertEqual(202, act.events[3].id)
        self.assertEqual(101, act.events[3].venue.id)

    def test_get_act_by_type_and_title_music_found(self):

        act = self.act_dao.query_for_act(
            self.session, act_type='music',
            search_type='Artist', title='Wynton Marsalis')

        self.assertEqual(304, act.id)
        self.assertEqual('Wynton Marsalis', act.title)
        self.assertEqual('Sketches of Spain', act.notes)
        self.assertEqual(Act.MUSIC, act.act_type)
        self.assertEqual(1, len(act.events))
        self.assertEqual(201, act.events[0].id)
        self.assertEqual(101, act.events[0].venue.id)

    def test_get_act_by_type_and_title_movie_found(self):

        act = self.act_dao.query_for_act(
            self.session, act_type='movie',
            search_type='Title', title='Wynton Marsalis')

        self.assertEqual(305, act.id)
        self.assertEqual('Wynton Marsalis', act.title)
        self.assertEqual('The History of Jazz', act.notes)
        self.assertEqual(Act.MOVIE, act.act_type)
        self.assertEqual(1, len(act.events))
        self.assertEqual(205, act.events[0].id)
        self.assertEqual(103, act.events[0].venue.id)

    def test_get_act_by_type_and_title_music_multiple_events(self):

        act = self.act_dao.query_for_act(
            self.session, act_type='music',
            search_type='Artist', title='Berlin Philharmonic')

        self.assertEqual(301, act.id)
        self.assertEqual('Berlin Philharmonic', act.title)
        self.assertEqual('Beethoven and Brahms', act.notes)
        self.assertEqual(1, act.act_type)
        self.assertEqual(4, len(act.events))
        # events are sorted by their date_time
        self.assertEqual(204, act.events[0].id)
        self.assertEqual(102, act.events[0].venue.id)
        self.assertEqual(201, act.events[1].id)
        self.assertEqual(101, act.events[1].venue.id)
        self.assertEqual(203, act.events[2].id)
        self.assertEqual(102, act.events[2].venue.id)
        self.assertEqual(202, act.events[3].id)
        self.assertEqual(101, act.events[3].venue.id)

    def test_get_act_and_events_found(self):

        act = self.act_dao.get_act_and_events(301, self.session)

        self.assertEqual(301, act.id)
        self.assertEqual('Berlin Philharmonic', act.title)
        self.assertEqual('Beethoven and Brahms', act.notes)
        self.assertEqual(1, act.act_type)
        self.assertEqual(4, len(act.events))
        # events are sorted by their date_time
        self.assertEqual(204, act.events[0].id)
        self.assertEqual(102, act.events[0].venue.id)
        self.assertEqual(201, act.events[1].id)
        self.assertEqual(101, act.events[1].venue.id)
        self.assertEqual(203, act.events[2].id)
        self.assertEqual(102, act.events[2].venue.id)
        self.assertEqual(202, act.events[3].id)
        self.assertEqual(101, act.events[3].venue.id)

    def test_get_act_not_found(self):
        self.assertRaises(
            PersistenceError, self.act_dao.delete, 999, self.session)

    def test_add_act_ok(self):
        act = Act(id=399, title='Joey Alexander', notes='Giant Steps',
                  act_type=1, year=2016)

        self.act_dao.add(act, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from acts where id = 399')
        self.assertEqual('Joey Alexander', rows[0][2])

    def test_update_act_ok(self):
        act = Act(id=304, title='Wynton Marsalis', notes='My Favorite Things',
                  act_type=2, year=2015)

        self.act_dao.update(act, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from acts where id = 304')
        self.assertEqual('My Favorite Things', rows[0][1])
        self.assertEqual('Wynton Marsalis', rows[0][2])
        self.assertEqual(2, rows[0][3])
        self.assertEqual(2015, rows[0][4])

    def test_delete_act_found(self):

        self.act_dao.delete(303, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from acts where id = 303')
        self.assertEqual(0, len(rows))

    def test_delete_act_not_found(self):
        self.assertRaises(
            PersistenceError, self.act_dao.delete, 999, self.session)

    # -------------------------------------------------------------------------
    #                        Set Up and Tear Down Methods
    # -------------------------------------------------------------------------

    @classmethod
    def tearDownClass(cls):
        """Called once, before the first test case is run"""
        os.remove(db_filename)

    def setUp(self):
        """Called before each test case"""
        create_db_tables(db_filename)
        self.populate_db_tables()

        settings = {'sqlalchemy.url': 'sqlite:///' + db_filename}
        # Create the SQLAlchemy DB Engine
        engine = engine_from_config(settings, 'sqlalchemy.')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.act_dao = ActDao()

    def tearDown(self):
        self.session.close_all()
        drop_db_tables(db_filename)

    # -------------------------------------------------------------------------
    #                              Utility Methods
    # -------------------------------------------------------------------------

    def populate_db_tables(self):
        execute_insert(db_filename, 'acts',
            # id, notes, title, act_type, year
            (301, 'Beethoven and Brahms', 'Berlin Philharmonic', Act.MUSIC, 0),
            (302, 'Unplugged', 'Eric Clapton', Act.MUSIC, 0),
            (303, 'Gershwin Rhapsody in Blue', 'New York Philharmonic', Act.MUSIC, 0),
            (304, 'Sketches of Spain', 'Wynton Marsalis', Act.MUSIC, 0),
            (305, 'The History of Jazz', 'Wynton Marsalis', Act.MOVIE, 0)
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
            (205, '2015-10-01 19:30:00.000', 103, None)
        )
        execute_insert(db_filename, 'venues',
            (101, 'Chicago', 'USA', 41.8369, -87.6847, 'Auditorium Theatre',
             'IL', 'E Congress Pkwy, Chicago, IL 60605'),
            (102, 'New York', 'USA', 40.7127, -74.0059, 'Carnegie Hall',
             'NY', '881 7th Ave, New York, NY 10019'),
            (103, 'Kingston', 'USA', 42.7127, -73.0059, 'Kingston Cinema 6',
             'NY', '1205 Ulster Ave, Kingston NY 12401')
        )
