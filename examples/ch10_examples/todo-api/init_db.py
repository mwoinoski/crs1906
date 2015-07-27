"""
init_db.py - Initialize a Sqlite3 database for the rest-server.py script.
"""

import sqlite3
conn = sqlite3.connect('rest_server.sqlite')
c = conn.cursor()

c.execute("""CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              password TEXT)""")
c.execute("""INSERT INTO users VALUES (1, 'student', 'studentpw')""")
c.execute("""INSERT INTO users VALUES (2, 'homer', 'homerpw')""")
c.execute("""INSERT INTO users VALUES (3, 'marge', 'margepw')""")
conn.commit()

c = conn.cursor()
c.execute("""CREATE TABLE todo_tasks
             (id integer primary key,
              title text,
              description text,
              done integer)""")
c.execute("""INSERT INTO todo_tasks
             VALUES (1,
                     'Teach cat Spanish',
                     'Needs to work on irregular verbs',
                     0)""")
c.execute("""INSERT INTO todo_tasks
             VALUES (2,
                     'Untangle Gordian knot',
                     'Remember what happened last time',
                     0)""")
conn.commit()

conn.close()
