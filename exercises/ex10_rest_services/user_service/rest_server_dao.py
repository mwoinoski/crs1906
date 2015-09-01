"""
rest_server_dao.py - DAO for REST server in rest_server.py
"""

import re
import sqlite3

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


users = [
    {
        "email": "ned.flanders@gmail.com",
        "first_name": "Ned",
        "middles": "Abraham",
        "last_name": "Flanders",
        "address": {
            "street": "125 Maple St",
            "post_code": "97478",
            "city": "Springfield",
            "state": "OR",
            "country": "USA",
        }
    },
    {
        "email": "monty.burns@burns.com",
        "first_name": "Montgomery",
        "middles": "Flint",
        "last_name": "Burns",
        "address": {
            "street": "1 Hill St",
            "post_code": "97478",
            "city": "Springfield",
            "state": "OR",
            "country": "USA",
        }
    },
]


def get_password(username):
    # pw = None
    # if re.match(r'^[A-Za-z0-9._-]+$', username):  # validate username
    #     conn = sqlite3.connect('rest_server.sqlite')
    #     c = conn.cursor()
    #     c.execute('SELECT password FROM users WHERE username=?', (username,))
    #     pw = c.fetchone()  # FIXME: add decryption
    #     pw = pw[0] if len(pw) > 0 else None
    # return pw
    return 'studentpw'


def get_all_users():
    # users = []
    # conn = sqlite3.connect('rest_server.db')
    # c = conn.cursor()
    # for row in c.execute('SELECT * FROM todo_users'):
    #     users.append(_make_user(row))
    return users


# def _make_user(row):
#     return {
#         "email": row[0],
#         "first_name": row[1],
#         "middles": row[2],
#         "last_name": row[3],
#         "address": {
#             "street": row[4],
#             "post_code": row[5],
#             "city": row[6],
#             "state": row[7],
#             "country": row[8],
#         }
#     }


def get_user(email):
    # conn = sqlite3.connect('rest_server.db')
    # c = conn.cursor()
    # c.execute('SELECT * FROM todo_users')
    # user_list = c.fetchone()
    user_list = [t for t in users if t['email'] == email]
    return user_list[0] if len(user_list) > 0 else None


def create_user(email, first_name, middles, last_name, street, post_code,
                city, state, country):
    # conn = sqlite3.connect('rest_server.db')
    # c = conn.cursor()
    # c.execute("""INSERT INTO todo_users VALUES (?, ?, ?)""",
    #           (title, description, 1 if done else 0))
    # FIXME: sanitize inputs
    user = {
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
    users.append(user)
    return user


def update_user(email, first_name, middles, last_name, street, post_code,
                city, state, country):
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
    return user


def delete_user(email):
    user_list = [t for t in users if t['email'] == email]
    if len(user_list) != 0:
        users.remove(user_list[0])
        return True
    return False
