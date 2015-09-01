"""
init_db.py - Initialize a Sqlite3 database for the rest-server.py script.
"""

import sqlite3
conn = sqlite3.connect('rest_server.sqlite')

c = conn.cursor()
c.execute("""CREATE TABLE person
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              password TEXT)""")
c.execute("""INSERT INTO users VALUES (1, 'student', 'studentpw')""")
c.execute("""INSERT INTO users VALUES (2, 'homer', 'homerpw')""")
c.execute("""INSERT INTO users VALUES (3, 'marge', 'margepw')""")
conn.commit()


conn.close()
