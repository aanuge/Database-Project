import os
from .swen344_db_utils import *
import hashlib
import secrets


def rebuild_tables():
    exec_sql_file('src/db/schema.sql')


def home_screen():
    return 'hello'


def list_all_users():
    return exec_get_all('SELECT username FROM users')


def list_communities_and_channels():
    results = ['comedy']
    results2 = list(exec_get_all('SELECT channel_name FROM comedy_channels'))
    results.append('arrakis')
    for x in results2:
        results.append(x[0])
    results2 = list(exec_get_all('SELECT channel_name FROM arrakis_channels'))
    for x in results2:
        results.append(x[0])
    return results


def list_dms(max_num):
    return exec_get_all("""SELECT content FROM messages LIMIT {}""".format(max_num))


def list_arrakis_messages(channel):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT id FROM arrakis_channels WHERE id = {}""".format(channel))
    result = cur.fetchall()
    conn.close()
    if len(result) == 0:
        return
    return exec_get_all('SELECT content FROM arrakis_messages WHERE channel_id = {}'.format(channel))


def list_comedy_messages(channel):
    return exec_get_all('SELECT content FROM comedy_messages WHERE channel_id = {}'.format(channel))


def send_dm(sender, recipient, content):
    conn = connect()
    cur = conn.cursor()
    send = """
        INSERT INTO messages(sender, recipient, content)
        VALUES((%s), (%s), (%s))
    """
    cur.execute(send, [sender, recipient, content])
    conn.commit()
    conn.close()


def add_user(username, password):
    conn = connect()
    cur = conn.cursor()
    add = """
        INSERT INTO users(username, password)
        VALUES((%s), (%s))
    """
    cur.execute("""SELECT username FROM users WHERE username = (%s)""", [username])
    result = cur.fetchall()
    if len(result) != 0:
        conn.close()
        return
    cur.execute(add, [username, password])
    conn.commit()
    conn.close()


def delete_user(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT session_key FROM users WHERE username = (%s)""", [username])
    key = cur.fetchall()
    if len(key) == 0:
        print('Not logged in')
        conn.close()
        return
    delete = """
        DELETE FROM users WHERE username = (%s)
    """
    cur.execute("""SELECT username FROM users WHERE username = (%s)""", [username])
    result = cur.fetchall()
    if len(result) == 0:
        conn.close()
        return
    cur.execute(delete, [username])
    conn.commit()
    conn.close()


def update_user(oldusername, newusername, newemail, newphone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT session_key FROM users WHERE username = (%s)""", [oldusername])
    key = cur.fetchall()
    if len(key) == 0:
        print('Not logged in')
        conn.close()
        return
    cur.execute("""SELECT username FROM users WHERE username = (%s)""", [oldusername])
    result = cur.fetchall()
    if len(result) == 0:
        conn.close()
        return
    cur.execute("""UPDATE users SET username = (%s) WHERE username = (%s)""", [newusername, oldusername])
    cur.execute("""UPDATE users SET email = (%s) WHERE username = (%s)""", [newemail, newusername])
    cur.execute("""UPDATE users SET phone = (%s) WHERE username = (%s)""", [newphone, newusername])
    conn.commit()
    conn.close()


def login(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT id FROM users WHERE username = (%s) AND password = (%s)""", [username, password])
    results = cur.fetchall()
    if len(results) == 1:
        session_key = secrets.token_hex(512)
        cur.execute("""UPDATE users SET session_key = (%s) WHERE username = (%s)""", [session_key, username])
        conn.commit()
        return session_key
    else:
        cur.execute("""SELECT password FROM users WHERE username = (%s)""", [username])
        conn.close()
        return 0


def logout(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT session_key FROM users WHERE username = (%s)""", [username])
    session_key = cur.fetchall()[0][0]
    if session_key is not None:
        cur.execute("""UPDATE users SET session_key = '' WHERE session_key = (%s)""", session_key)
        conn.commit()
    conn.close()
