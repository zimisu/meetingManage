import json

from flask import Flask

app = Flask(__name__)
TOKEN = 'baixingg5'


"""------ Read credential settings ------"""
cred = {}
with open('cred.json', 'r') as f:
    cred.update(json.load(f))
    print(cred)

