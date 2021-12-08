"""
rest_server_dao.py - DAO for REST server in rest_server.py
"""

import re
import sqlite3

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


# The Sqlite database is defined in the file users_db.sqlite
# Manage the database with the Sqlite CLI: see https://www.sqlite.org/cli.html
# sqlite3 users_db.sqlite
# .help
# .tables
# .schema users
# select * from users;
# .quit

# The users table looks like this:
# id|username|password|email|first_name|middles|last_name|street|post_code|city|state|country
# 1|nedf|nedfpw|ned.flanders@gmail.com|Ned|Abraham|Flanders|125 Maple St|97478|Springfield|OR|USA
# 2|montyb|montybpw|monty.burns@burns.com|Montgomery|Flint|Burns|1 Hill St|97478|Springfield|OR|USA


def get_password(username):
    sql = """
        SELECT password 
          FROM users 
         WHERE username = ?
    """
    if re.match(r'^[A-Za-z0-9._-]+$', username):  # validate username
        conn, c = init_operation()
        c.execute(sql, (username,))
        pw = c.fetchone()  # BETTER: add decryption
        pw = pw[0] if pw and len(pw) > 0 else None
        end_operation(conn, c)
        return pw
    else:
        raise ValueError(f'invalid username {username}')


def get_all_users():
    sql = """
        SELECT id,username,password,email,first_name,middles,last_name,
               street,post_code,city,state,country
          FROM users
    """
    conn, c = init_operation()
    users = [_make_user_from_row(row) for row in c.execute(sql)]
    end_operation(conn, c)
    return users


def _make_user(user_id, username, password, email, first_name, middles, last_name,
               street, post_code, city, state, country):
    return {
        "id": user_id,
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "middles": middles,
        "last_name": last_name,
        "address": {
            "street": street,
            "post_code": post_code,
            "city": city,
            "state": state,
            "country": country,
        }
    }


def _make_user_from_row(row):
    return _make_user(*row)


def get_user(email):
    sql = """
        SELECT id,username,password,email,first_name,middles,last_name,
               street,post_code,city,state,country
        FROM users 
        WHERE email = ?
    """
    conn, c = init_operation()
    c.execute(sql, (email,))
    user = c.fetchone()
    end_operation(conn, c)
    return _make_user_from_row(user) if user else None


def create_user(username, password, email, first_name, middles, last_name,
                street, post_code, city, state, country):
    sql = """
        INSERT INTO users
            (username,password,email,first_name,middles,last_name,
             street,post_code,city,state,country)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (username, password, email, first_name, middles, last_name,
              street, post_code, city, state, country)

    conn, c = init_operation()
    c.execute(sql, values)
    c.execute('SELECT last_insert_rowid()')  # fetch auto-generated key
    user_id = c.fetchone()[0]
    end_operation(conn, c)

    user = _make_user_from_row((user_id,) + values)
    return user


def update_user(email, first_name, middles, last_name, street, post_code,
                city, state, country):
    sql = """
        UPDATE users
           SET first_name = ?,
               middles = ?,
               last_name = ?,
               street = ?,
               post_code = ?,
               city = ?,
               state = ?,
               country = ?
         WHERE email = ?
    """
    user = get_user(email)
    if user is not None:
        if first_name is not None:
            user['first_name'] = first_name
        if middles is not None:
            user['middles'] = middles
        if last_name is not None:
            user['last_name'] = last_name
        if street is not None:
            user['address']['street'] = street
        if post_code is not None:
            user['address']['post_code'] = post_code
        if city is not None:
            user['address']['city'] = city
        if state is not None:
            user['address']['state'] = state
        if country is not None:
            user['address']['country'] = country
            
        values = (
            user['first_name'], user['middles'], user['last_name'],
            user['address']['street'], user['address']['post_code'],
            user['address']['city'], user['address']['state'],
            user['address']['country'], email
        )

        conn, c = init_operation()
        c.execute(sql, values)
        end_operation(conn, c)
        return user
    else:
        raise ValueError(f'unknown user email {email}')


def delete_user(email):
    sql = """
        DELETE FROM users
         WHERE email = ?
    """
    conn, c = init_operation()
    c.execute(sql, (email,))
    c.execute('SELECT changes()')  # fetch number of rows deleted
    row_count = c.fetchone()[0]
    end_operation(conn, c)
    return row_count > 0


# Test cases can change Sqlite database file name to test different conditions
sqlite_file_name = 'users_db.sqlite'


def init_operation():
    conn = sqlite3.connect(sqlite_file_name)
    cursor = conn.cursor()
    return conn, cursor


def end_operation(conn, cursor):
    cursor.close()
    conn.commit()
