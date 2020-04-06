"""
rest_server_dao.py - DAO for REST server in rest_server.py
"""
import re
import sqlite3

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

# Manage a SQLite database.
# To connect to the DB file and run SQL commands:
# cd \crs1906\examples\ch09_examples\todo-api\
# \software\sqlite\sqlite3 rest_server.sqlite
# .tables
conn = sqlite3.connect('rest_server.sqlite', check_same_thread=False)


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
    return [_make_task(row) for row in cursor.execute(sql)]


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
    return cursor.fetchone()


def create_task(title, description, done):
    global conn
    sql = """
        INSERT INTO todo_tasks 
        (title, description, done)
        VALUES (?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(sql, (title, description, 1 if done else 0))
    conn.commit()

    task = {
        'id': cursor.lastrowid,
        'title': title,
        'description': description,
        'done': done
    }
    return task


def update_task(task_id, title, description, done):
    global conn
    update_title_sql = 'UPDATE todo_tasks SET title = ? WHERE id = ?'
    update_description_sql = 'UPDATE todo_tasks SET description = ? WHERE id = ?'
    update_done_sql = 'UPDATE todo_tasks SET done = ? WHERE id = ?'
    cursor = conn.cursor()
    if title:
        cursor.execute(update_title_sql, (title, task_id))
    if description:
        cursor.execute(update_description_sql, (description, task_id))
    if done is not None:
        cursor.execute(update_done_sql, (1 if done else 0, task_id))
    conn.commit()

    task_fields = ('id', 'title', 'description', 'done')
    db_task = get_task(task_id)
    task = {k: v for k, v in zip(task_fields, db_task)}
    return task


def delete_task(task_id):
    global conn
    sql = """
        DELETE FROM todo_tasks 
        WHERE id = ?
    """
    cursor = conn.cursor()
    cursor.execute(sql, (task_id,))
    conn.commit()
    return bool(cursor.rowcount)
