import json
import os
import sys
import hashlib

myDir = os.getcwd()
sys.path.append(myDir)

from flask import request
from flask_restful import Resource, reqparse, request
from src.db import chat_db


class rebuild_tables(Resource):
    def get(self):
        rebuild_tables()


class home_screen(Resource):
    def get(self):
        return chat_db.home_screen()


class list_all_users(Resource):
    def get(self):
        return chat_db.list_all_users()


class list_communities_and_channels(Resource):
    def get(self):
        return chat_db.list_communities_and_channels()


class list_arrakis_messages(Resource):
    def get(self, id):
        return chat_db.list_arrakis_messages(id)


class list_comedy_messages(Resource):
    def get(self, id):
        return chat_db.list_comedy_messages(id)


class add_user(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        encoded = password.encode('utf-8')
        hashed_password = hashlib.sha512(encoded).hexdigest()
        return chat_db.add_user(username, hashed_password)


class delete_user(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        username = args['username']
        return chat_db.delete_user(username)


class update_user(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oldusername', type=str)
        parser.add_argument('newusername', type=str)
        parser.add_argument('newemail', type=str)
        parser.add_argument('newphone', type=str)
        args = parser.parse_args()
        oldusername = args['oldusername']
        newusername = args['newusername']
        newemail = args['newemail']
        newphone = args['newphone']
        return chat_db.update_user(oldusername, newusername, newemail, newphone)


class login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        encoded = password.encode('utf-8')
        hashed_password = hashlib.sha512(encoded).hexdigest()
        return chat_db.login(username, hashed_password)


class logout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        username = args['username']
        return chat_db.logout(username)


class list_dms(Resource):
    def get(self, num):
        return chat_db.list_dms(num)


class send_dm(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sender', type=str)
        parser.add_argument('recipient', type=str)
        parser.add_argument('content', type=str)
        args = parser.parse_args()
        sender = args['sender']
        recipient = args['recipient']
        content = args['content']
        return chat_db.send_dm(sender, recipient, content)
