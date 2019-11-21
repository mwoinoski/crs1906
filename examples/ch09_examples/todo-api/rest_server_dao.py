"""
rest_server_dao.py - DAO for REST server in rest_server.py
"""
import re
import sqlite3

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


conn = sqlite3.connect('rest_server.db')


def get_password(username):
    global conn
    sql_get_password = """
        SELECT password 
          FROM users 
         WHERE username = ?
    """
    pw = None
    if re.match(r'^[A-Za-z0-9._-]+$', username):  # validate username
        c = conn.cursor()
        c.execute(sql_get_password, (username,))
        pw = c.fetchone()  # TODO: add decryption
        pw = pw[0] if len(pw) > 0 else None
    return pw


def get_all_tasks():
    global conn
    sql = """
        SELECT id, title, description, done
        FROM todo_tasks
    """
    cursor = conn.cursor()
    for row in cursor.execute(sql):
        yield _make_task(row)


def _make_task(row):
    return {'id': row[0],
            'title': row[1],
            'description': row[2],
            'done': row[3] != 0}


def get_task(task_id):
    global conn
    sql = """
        SELECT id, title, description, done 
          FROM todo_tasks
         WHERE id = ?
    """
    cursor = conn.cursor()
    cursor.execute(sql, (task_id,))
    task_list = cursor.fetchone()
    return task_list[0] if len(task_list) > 0 else None


def create_task(title, description, done):
    # TODO: sanitize inputs
    global conn
    sql = """
        INSERT INTO todo_tasks 
        VALUES (?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(sql, (title, description, 1 if done else 0))

    task = {
        'id': cursor.lastrowid,
        'title': title,
        'description': description,
        'done': done
    }
    return task


def update_task(task_id, title, description, done):
    global conn
    sql = """
        UPDATE todo_tasks 
        SET title = ?, description = ?, done = ?
        WHERE id = ?
    """
    cursor = conn.cursor()
    cursor.execute(sql, (title, description, 1 if done else 0, task_id))

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
    global conn
    sql = """
        DELETE FROM todo_tasks 
        WHERE id = ?
    """
    cursor = conn.cursor()
    cursor.execute(sql, (task_id,))
    return bool(cursor.rowcount)
