"""
Integration tests for VenueDao.
"""
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from sqlalchemy.orm import sessionmaker

from unittest import TestCase
from ticketmanor import engine_from_config
from tests.test_support.db_utils import (
    create_db_tables,
    drop_db_tables,
    execute_select,
    execute_insert,
)
from ticketmanor.models.venue import Venue
from ticketmanor.models.persistence.venue_dao import VenueDao
# The following import for Event is required. PyCharm flags it as unused, but
# without it, SQLAlchemy raises exceptions.
from ticketmanor.models.event import Event

# SQLAlchemy can't connect to an in-memory SQLite database, so we'll
# use a temporary database file.
db_filename = 'test_db.sqlite'


class VenueDaoTest(TestCase):
    """
    Integration tests for VenueDao
    """

    # -------------------------------------------------------------------------
    #                              Test Cases
    # -------------------------------------------------------------------------

    def test_get_venue_found(self):

        venue = self.venue_dao.get(101, self.session)

        self.assertEqual(101, venue.id)
        self.assertEqual('Chicago', venue.city)
        self.assertEqual('USA', venue.country)
        self.assertEqual(41.8369, venue.latitude)
        self.assertEqual(-87.6847, venue.longitude)
        self.assertEqual('Auditorium Theatre', venue.name)
        self.assertEqual('IL', venue.prov_state)
        self.assertEqual('E Congress Pkwy, Chicago, IL 60605',
                         venue.street_address)
        self.assertEqual(2, len(venue.events))
        self.assertEqual(201, venue.events[0].id)
        self.assertEqual(202, venue.events[1].id)

    def test_get_venue_by_name_found(self):

        venue = self.venue_dao.get_venue_by_name('Auditorium Theatre',
                                                 self.session)

        self.assertEqual(101, venue.id)
        self.assertEqual('Chicago', venue.city)
        self.assertEqual('USA', venue.country)
        self.assertEqual(41.8369, venue.latitude)
        self.assertEqual(-87.6847, venue.longitude)
        self.assertEqual('Auditorium Theatre', venue.name)
        self.assertEqual('IL', venue.prov_state)
        self.assertEqual('E Congress Pkwy, Chicago, IL 60605',
                         venue.street_address)
        self.assertEqual(2, len(venue.events))
        self.assertEqual(201, venue.events[0].id)
        self.assertEqual(202, venue.events[1].id)

    def test_get_venue_and_events_found(self):

        venue = self.venue_dao.get_venue_and_events(101, self.session)

        self.assertEqual(101, venue.id)
        self.assertEqual('Chicago', venue.city)
        self.assertEqual('USA', venue.country)
        self.assertEqual(41.8369, venue.latitude)
        self.assertEqual(-87.6847, venue.longitude)
        self.assertEqual('Auditorium Theatre', venue.name)
        self.assertEqual('IL', venue.prov_state)
        self.assertEqual('E Congress Pkwy, Chicago, IL 60605',
                         venue.street_address)
        self.assertEqual(2, len(venue.events))
        self.assertEqual(201, venue.events[0].id)
        self.assertEqual(202, venue.events[1].id)

    def test_get_venue_not_found(self):

        self.assertRaises(PersistenceError, self.venue_dao.delete, 999,
                          self.session)

    def test_add_venue_ok(self):

        venue = Venue(id=678, city='London', country='UK', latitude=51.5072,
                      longitude=-0.1275, name='Royal Albert Hall',
                      street_address='Kensington Gore, London SW7 2AP')

        self.venue_dao.add(venue, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from venues where id = 678')
        self.assertEqual('Royal Albert Hall', rows[0][5])

    def test_update_venue_ok(self):
        venue = Venue(id=678, city='London', country='United Kingdom',
                      latitude=51.5072, longitude=-0.1275,
                      name='Royal Albert Hall',
                      street_address='Kensington Gore, London SW7 2AP')

        self.venue_dao.update(venue, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from venues where id = 678')
        self.assertEqual('United Kingdom', rows[0][2])

    def test_delete_venue_found(self):
        self.venue_dao.delete(101, self.session)
        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from venues where id = 101')

        self.assertEqual(0, len(rows))

    def test_delete_venue_not_found(self):

        self.assertRaises(PersistenceError, self.venue_dao.delete, 999,
                          self.session)

    # -------------------------------------------------------------------------
    #                        Set Up and Tear Down Methods
    # -------------------------------------------------------------------------

    def setUp(self):
        create_db_tables(db_filename)
        self.populate_db_tables()

        settings = {'sqlalchemy.url': 'sqlite:///' + db_filename}
        # Create the SQLAlchemy DB Engine
        engine = engine_from_config(settings, 'sqlalchemy.')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.venue_dao = VenueDao()

    def tearDown(self):
        self.session.close_all()
        #self.session.close_all_sessions()
        drop_db_tables(db_filename)

    # -------------------------------------------------------------------------
    #                              Utility Methods
    # -------------------------------------------------------------------------

    def populate_db_tables(self):
        execute_insert(db_filename, 'events',
            (201, '2015-12-31 20:00:00.000', 101, None),
            (202, '2016-01-01 20:00:00.000', 101, None),
            (203, '2015-12-31 21:00:00.000', 102, None),
            (204, '2015-12-25 10:00:00.000', 102, None)
        )
        execute_insert(db_filename, 'venues',
            (101, 'Chicago', 'USA', 41.8369, -87.6847, 'Auditorium Theatre',
             'IL', 'E Congress Pkwy, Chicago, IL 60605'),
            (102, 'New York', 'USA', 40.7127, -74.0059, 'Carnegie Hall',
             'NY', '881 7th Ave, New York, NY 10019')
        )
