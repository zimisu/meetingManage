import json

from flask import Flask
from flask.ext.pymongo import PyMongo
from flask_socketio import SocketIO
from memcache import Client

app = Flask('chidao')
TOKEN = 'baixingg5'

app.secret_key = TOKEN

mongo = PyMongo(app)

sio = SocketIO(app)

mc = Client(['127.0.0.1:12000'], debug=0)


"""------ Read credential settings ------"""
cred = {}
with open('cred.json', 'r') as f:
    cred.update(json.load(f))
    print(cred)

