import json

from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask('chidao')
TOKEN = 'baixingg5'

mongo = PyMongo(app)


"""------ Read credential settings ------"""
cred = {}
with open('cred.json', 'r') as f:
    cred.update(json.load(f))
    print(cred)

