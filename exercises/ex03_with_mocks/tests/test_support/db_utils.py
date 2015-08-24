"""
Database utility functions.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import sys
import sqlite3


def create_db_tables(db):
    """
    Create all database tables in the TicketManor schema

    :param db: name of SQLite database file
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Schema was created from MySQL dump.
    # Schema required these changes:
    #   bigint(20) NOT NULL AUTO_INCREMENT --> INTEGER PRIMARY KEY
    #   remove PRIMARY KEY (id)
    #   remove CONSTRAINT

    c.execute('''CREATE TABLE acts (
        id INTEGER PRIMAY KEY,
        notes varchar(255) DEFAULT NULL,
        title varchar(255) DEFAULT NULL,
        type int(11) DEFAULT NULL,
        year int(11) NOT NULL
        )''')

    c.execute('''CREATE TABLE acts_events (
        acts_id bigint(20) NOT NULL,
        events_id bigint(20) NOT NULL,
        FOREIGN KEY (events_id) REFERENCES events (id),
        FOREIGN KEY (acts_id) REFERENCES acts (id)
        )''')

    c.execute('''CREATE TABLE admin (
        id INTEGER PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES people (id)
        )''')

    c.execute('''CREATE TABLE auditoriums (
        id INTEGER PRIMARY KEY,
        address varchar(255) DEFAULT NULL,
        name varchar(255) DEFAULT NULL,
        venue_id bigint(20) DEFAULT NULL,
        FOREIGN KEY (venue_id) REFERENCES venues (id)
        )''')

    c.execute('''CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES people (id)
        )''')

    c.execute('''CREATE TABLE events (
        id INTEGER PRIMARY KEY,
        date_time date_time default null,
        venue_id bigint(20) DEFAULT NULL,
        what_id bigint(20) DEFAULT NULL,
        FOREIGN KEY (what_id) REFERENCES acts (id),
        FOREIGN KEY (venue_id) REFERENCES venues (id)
        )''')

    c.execute('''CREATE TABLE feedbackform (
        id INTEGER PRIMARY KEY,
        comment varchar(255) DEFAULT NULL,
        custEmail varchar(255) DEFAULT NULL,
        custName varchar(255) DEFAULT NULL,
        date text
        )''')

    c.execute('''CREATE TABLE members (
        profilePhoto blob,
        id INTEGER PRIMARY KEY,
        nickName varchar(45) DEFAULT NULL,
        FOREIGN KEY (id) REFERENCES people (id)
        )''')

    c.execute('''CREATE TABLE movies (
        director varchar(255) DEFAULT NULL,
        id INTEGER PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES acts (id)
        )''')

    c.execute('''CREATE TABLE order_items (
        id INTEGER PRIMARY KEY,
        quantity int(11) NOT NULL,
        sellable_id bigint(20) DEFAULT NULL,
        FOREIGN KEY (sellable_id) REFERENCES sellable (id)
        )''')

    c.execute('''CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        member_id bigint(20) DEFAULT NULL,
        FOREIGN KEY (member_id) REFERENCES members (id)
        )''')

    c.execute('''CREATE TABLE orders_order_items (
        orders_id bigint(20) NOT NULL,
        items_id bigint(20) NOT NULL,
        FOREIGN KEY (orders_id) REFERENCES orders (id),
        FOREIGN KEY (items_id) REFERENCES order_items (id)
        )''')

    c.execute('''CREATE TABLE people (
        id INTEGER PRIMAY KEY,
        city varchar(255) DEFAULT NULL,
        country varchar(255) DEFAULT NULL,
        postcode varchar(255) DEFAULT NULL,
        state varchar(255) DEFAULT NULL,
        street varchar(255) DEFAULT NULL,
        email varchar(255) DEFAULT NULL,
        firstName varchar(255) NOT NULL,
        lastName varchar(255) NOT NULL,
        middles varchar(255) DEFAULT NULL
        )''')

    c.execute('''CREATE TABLE sellable (
        id INTEGER PRIMARY KEY,
        price double NOT NULL
        )''')

    c.execute('''CREATE TABLE tickets (
        price double DEFAULT NULL,
        seatNumber varchar(255) DEFAULT NULL,
        id INTEGER PRIMARY KEY,
        event_id bigint(20) NOT NULL,
        FOREIGN KEY (event_id) REFERENCES events (id),
        FOREIGN KEY (id) REFERENCES sellable (id)
        )''')

    c.execute('''CREATE TABLE venues (
        id INTEGER PRIMARY KEY,
        city varchar(255) DEFAULT NULL,
        country varchar(255) DEFAULT NULL,
        lat double DEFAULT NULL,
        lng double DEFAULT NULL,
        name varchar(255) DEFAULT NULL,
        provState varchar(255) DEFAULT NULL,
        streetAddress varchar(255) DEFAULT NULL
        )''')

    c.close()
    conn.close()


def drop_db_tables(db):
    """
    Drops all database tables created in create_db_tables().

    :param db: name of SQLite database file
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('''DROP TABLE acts''')
    c.execute('''DROP TABLE acts_events''')
    c.execute('''DROP TABLE admin''')
    c.execute('''DROP TABLE auditoriums''')
    c.execute('''DROP TABLE customers''')
    c.execute('''DROP TABLE events''')
    c.execute('''DROP TABLE feedbackform''')
    c.execute('''DROP TABLE members''')
    c.execute('''DROP TABLE movies''')
    c.execute('''DROP TABLE order_items''')
    c.execute('''DROP TABLE orders''')
    c.execute('''DROP TABLE orders_order_items''')
    c.execute('''DROP TABLE people''')
    c.execute('''DROP TABLE sellable''')
    c.execute('''DROP TABLE tickets''')
    c.execute('''DROP TABLE venues''')

    conn.commit()
    c.close()
    conn.close()


def execute_select(db, sql):
    """
    Executes a SQL SELECT statement.
    :param db: name of SQLite database file
    :param sql: SQL SELECT statement to execute
    :return: list of selected rows
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    c.close()
    conn.close()
    return rows

def execute_insert(db, table_name, *values):
    """
    Executes one or more SQL INSERT statements.
    :param table_name: name of table where INSERT will occur
    :param values: list of tuples of values to be inserted.
           Use None for a null value.
    """
    statements = ['INSERT INTO {} VALUES ({})'.format(table_name,
        ','.join("'" + v + "'" if isinstance(v, str) else 'null' if v is None else str(v)
                 for v in value_tuple)) for value_tuple in values]

    # Or, if you prefer a non-Pythonic approach:
    # statements = []
    # for value_tuple in values:
    #     value_list = []
    #     for v in value_tuple:
    #         if isinstance(v, str):
    #             v_str = "'" + v + "'"
    #         elif v is None:
    #             v_str = 'null'
    #         else:
    #             v_str = str(v)
    #         value_list.append(v_str)
    #     value_str = ','.join(value_list)
    #     statement = 'INSERT INTO {} VALUES ({})'.format(table_name, value_str)
    #     statements.append(statement)
    execute_sql(db, *statements)


def execute_sql(db, *sql):
    """
    Executes one or more SQL INSERT, UPDATE, or DELETE statements.
    :param db: name of SQLite database file
    :param sql: list of SQL statements to execute
    """
    conn = sqlite3.connect(db)
    with conn:  # commits automatically if no exception
        c = conn.cursor()
        for stmt in sql:
            c.execute(stmt)
        c.close()
    conn.close()
