"""
rest_server_dao.py - DAO for REST server in rest_server.py
"""
import re
import sqlite3

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


tasks = [
    {
        'id': 1,
        'title': 'Teach cat Spanish',
        'description': 'Needs to work on irregular verbs',
        'done': False
    },
    {
        'id': 2,
        'title': 'Untangle Gordian knot',
        'description': 'Remember what happened last time',
        'done': False
    }
]

_next_task_id = len(tasks) + 1


def get_password(username):
    pw = None
    if re.match(r'^[A-Za-z0-9._-]+$', username):  # validate username
        conn = sqlite3.connect('rest_server.sqlite')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username=?', (username,))
        pw = c.fetchone()  # TODO: add decryption
        pw = pw[0] if len(pw) > 0 else None
    return pw


def get_all_tasks():
    # tasks = []
    # conn = sqlite3.connect('rest_server.db')
    # c = conn.cursor()
    # for row in c.execute('SELECT * FROM todo_tasks'):
    #     tasks.append(_make_task(row))
    return tasks

def _make_task(row):
    return {'id': row[0],
            'title': row[1],
            'description': row[2],
            'done': row[3] != 0}

def get_task(task_id):
    # conn = sqlite3.connect('rest_server.db')
    # c = conn.cursor()
    # c.execute('SELECT * FROM todo_tasks')
    # task_list = c.fetchone()
    task_list = [t for t in tasks if t['id'] == task_id]
    return task_list[0] if len(task_list) > 0 else None


def create_task(title, description, done):
    # conn = sqlite3.connect('rest_server.db')
    # c = conn.cursor()
    # c.execute("""INSERT INTO todo_tasks VALUES (?, ?, ?)""",
    #           (title, description, 1 if done else 0))
    # TODO: sanitize inputs
    global _next_task_id
    task = {
        'id': _next_task_id,
        'title': title,
        'description': description,
        'done': done
    }
    _next_task_id += 1
    tasks.append(task)
    return task


def update_task(task_id, title, description, done):
    task = get_task(task_id)
    if task is not None:
        if title is not None:
            task['title'] = title
        if description is not None:
            task['description'] = description
        if done is not None:
            task['done'] = done
    return task


def delete_task(task_id):
    task_list = [t for t in tasks if t['id'] == task_id]
    if len(task_list) != 0:
        tasks.remove(task_list[0])
        return True
    return False
