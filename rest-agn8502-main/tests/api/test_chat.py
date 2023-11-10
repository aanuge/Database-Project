import unittest
from tests.test_utils import *
from src.db.chat_db import rebuild_tables
import hashlib


class TestChat(unittest.TestCase):
    base_url = 'http://localhost:5000'

    def setUp(self):
        rebuild_tables()

    def test_list_all_users(self):
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 9)

    def test_list_communities_and_channels(self):
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_communities_and_channels')
        self.assertEqual(len(result), 6)

    def test_list_channel_messages(self):
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_arrakis_messages/2')
        self.assertEqual(len(result), 2)

    def test_list_nonexistent_channel_messages(self):
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_arrakis_messages/3')
        self.assertIsNone(result)

    def test_list_dms(self):
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_dms/3')
        self.assertEqual(len(result), 3)

    def test_send_dm(self):
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_dms/100')
        self.assertEqual(len(result), 11)
        post_rest_call(self, 'http://127.0.0.1:5000/send_dm', params={"sender": "Abbott", "recipient": "Costello", "content": "abcdefghijklmnop"})
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_dms/100')
        self.assertEqual(len(result), 12)

    def test_login(self):
        conn = connect()
        cur = conn.cursor()
        password = '123'
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "test_user", "password": password})
        result = post_rest_call(self, 'http://127.0.0.1:5000/login', params={"username": "test_user", "password": password})
        cur.execute("""SELECT session_key FROM users WHERE username = 'test_user'""")
        session_key = cur.fetchall()[0][0]
        self.assertEqual(result, session_key)
        conn.close()

    def test_add(self):
        password = '123'
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "test_user", "password": password})
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT username FROM users WHERE username = 'test_user'""")
        self.assertEqual(cur.fetchall()[0][0], 'test_user')
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 10)
        conn.close()

    def test_add_existent(self):
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "Paul", "password": "123"})
        conn = connect()
        cur = conn.cursor()
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 9)
        print('Username already exists')
        conn.close()

    def test_delete(self):
        conn = connect()
        cur = conn.cursor()
        password = '123'
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "test_user", "password": password})
        post_rest_call(self, 'http://127.0.0.1:5000/login', params={"username": "test_user", "password": password})
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "test_user2", "password": "123"})
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 11)
        delete_rest_call(self, 'http://127.0.0.1:5000/delete', params={"username": "test_user2"})
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 10)
        delete_rest_call(self, 'http://127.0.0.1:5000/delete', params={"username": "test_user2"})
        conn.close()

    def test_delete_nonexistent(self):
        conn = connect()
        cur = conn.cursor()
        password = '123'
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "test_user", "password": password})
        post_rest_call(self, 'http://127.0.0.1:5000/login', params={"username": "test_user", "password": password})
        delete_rest_call(self, 'http://127.0.0.1:5000/delete', params={"username": "test_user"})
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 9)
        print("User does not exist")
        conn.close()

    def test_update(self):
        conn = connect()
        cur = conn.cursor()
        put_rest_call(self, 'http://127.0.0.1:5000/update',
                      params={"oldusername": "Paul", "newusername": "Rick", "newemail": "user@email.com",
                              "newphone": "012-345-6789"})
        cur.execute("""SELECT username FROM users WHERE id = 9""")
        result = cur.fetchall()[0][0]
        self.assertEqual(result, 'Rick')
        conn.close()

    def test_update_nonexistent(self):
        conn = connect()
        cur = conn.cursor()
        password = '123'
        post_rest_call(self, 'http://127.0.0.1:5000/add', params={"username": "test_user", "password": password})
        post_rest_call(self, 'http://127.0.0.1:5000/login', params={"username": "test_user", "password": password})
        put_rest_call(self, 'http://127.0.0.1:5000/update',
                      params={"oldusername": "test_user2", "newusername": "Rick", "newemail": "user@email.com",
                              "newphone": "012-345-6789"})
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        for i in result:
            self.assertNotEqual(i[0], 'Rick')
        print("User does not exist")
        conn.close()

    def test_remove_unauthenticated(self):
        conn = connect()
        cur = conn.cursor()
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 9)
        delete_rest_call(self, 'http://127.0.0.1:5000/delete', params={"username": "test_user"})
        result = get_rest_call(self, 'http://127.0.0.1:5000/list_all_users')
        self.assertEqual(len(result), 9)
        print('Not logged in')
        conn.close()


