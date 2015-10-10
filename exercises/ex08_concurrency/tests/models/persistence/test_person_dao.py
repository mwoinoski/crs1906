"""
Integration tests for PersonDao.
"""
from ticketmanor.models.persistence import PersistenceError

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import os
from sqlalchemy.orm import sessionmaker

from unittest import TestCase
from ticketmanor import engine_from_config
from tests.test_support.db_utils import (
    create_db_tables,
    drop_db_tables,
    execute_select,
    execute_insert,
)
from ticketmanor.models.person import Person
from ticketmanor.models.persistence.person_dao import PersonDao
# The following import for Event is required. PyCharm flags it as unused, but
# without it, SQLAlchemy raises exceptions.


# SQLAlchemy can't connect to an in-memory SQLite database, so we'll
# use a temporary database file.
db_filename = 'ticketmanor_db.sqlite'


class PersonDaoTest(TestCase):
    """
    Integration tests for PersonDao
    """

    # -------------------------------------------------------------------------
    #                              Test Cases
    # -------------------------------------------------------------------------

    def test_get_person_found(self):

        person = self.person_dao.get('hsimpson@gmail.com', self.session)

        self.assertEqual(101, person.id)
        self.assertEqual('Springfield', person.city)
        self.assertEqual('USA', person.country)
        self.assertEqual('54321', person.post_code)
        self.assertEqual('OR', person.state)
        self.assertEqual('123 Python St', person.street)
        self.assertEqual('hsimpson@gmail.com', person.email)
        self.assertEqual('Homer', person.first_name)
        self.assertEqual('Simpson', person.last_name)
        self.assertEqual('Virgil', person.middles)

    def test_get_person_not_found(self):

        self.assertRaises(PersistenceError, self.person_dao.delete, 999,
                          self.session)

    def test_add_person_ok(self):

        person = Person(id=103, city='Wigan', country='UK',
                        post_code='WG7 7FU', street='62 West Wallaby St',
                        email='wallace@wandg.com', first_name='Wallace',
                        middles='Peter', last_name='Sallis')

        self.person_dao.add(person, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from people where id = 103')
        self.assertEqual('Wallace', rows[0][7])

    def test_update_person_ok(self):
        person = Person(id=103, city='Wigan', country='UK',
                        post_code='WG7 7FU', street='62 West Wallaby St',
                        email='wallace@wandg.com', first_name='Wallace',
                        middles='Dwight', last_name='Schultz')

        self.person_dao.update(person, self.session)

        self.session.commit()

        rows = execute_select(db_filename,
                              'select * from people where id = 103')

        self.assertEqual('Dwight', rows[0][9])
        self.assertEqual('Schultz', rows[0][8])

    def test_delete_person_found(self):

        self.person_dao.delete('hsimpson@gmail.com', self.session)

        self.session.commit()

        rows = execute_select(
            db_filename,
            "select * from people where email = 'hsimpson@gmail.com'")

        self.assertEqual(0, len(rows))

    def test_delete_person_not_found(self):

        self.assertRaises(PersistenceError, self.person_dao.delete, 999,
                          self.session)

    # -------------------------------------------------------------------------
    #                        Set Up and Tear Down Methods
    # -------------------------------------------------------------------------

    @classmethod
    def tearDownClass(cls):
        os.remove(db_filename)

    def setUp(self):
        create_db_tables(db_filename)
        self.populate_db_tables()

        settings = {'sqlalchemy.url': 'sqlite:///' + db_filename}
        # Create the SQLAlchemy DB Engine
        engine = engine_from_config(settings, 'sqlalchemy.')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.person_dao = PersonDao()

    def tearDown(self):
        self.session.close_all()
        drop_db_tables(db_filename)

    # -------------------------------------------------------------------------
    #                              Utility Methods
    # -------------------------------------------------------------------------

    def populate_db_tables(self):
        execute_insert(db_filename, 'people',
            (101, 'Springfield', 'USA', '54321', 'OR', '123 Python St',
             'hsimpson@gmail.com', 'Homer', 'Simpson', 'Virgil'),
            (102, 'Springfield', 'USA', '54321', 'OR', '125 Python St',
             'nflanders@gmail.com', 'Ned', 'Flanders', 'Micah'),
        )
