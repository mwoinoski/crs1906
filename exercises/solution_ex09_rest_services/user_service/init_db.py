"""
init_db.py - Initialize a Sqlite3 database for the rest-server.py script.
"""

import sqlite3
conn = sqlite3.connect('rest_server.sqlite')

c = conn.cursor()
c.execute("""CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              password TEXT,
              email TEXT,
              first_name TEXT,
              middles TEXT,
              last_name TEXT,
              street TEXT,
              post_code TEXT,
              city TEXT,
              state TEXT,
              country TEXT)""")
c.execute("""INSERT INTO users 
             VALUES (1, 'nedf', 'nedfpw', 'ned.flanders@gmail.com', 'Ned', 'Abraham', 'Flanders', 
                     '125 Maple St', '97478', 'Springfield', 'OR', 'USA')""")
c.execute("""INSERT INTO users 
            VALUES (2, 'montyb', 'montybpw', 'monty.burns@burns.com', 'Montgomery', 'Flint', 'Burns', 
                    '1 Hill St', '97478', 'Springfield', 'OR', 'USA')""")
conn.commit()
conn.close()
