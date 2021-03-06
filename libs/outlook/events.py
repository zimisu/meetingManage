from collections import OrderedDict
from pprint import pprint

import requests
from pymongo import ReturnDocument

from app import mongo
from libs.oauth import get_token
from libs.outlook import graph
from libs.utility import process_meeting_data
import json


def get_events_by_wxid(u):
    headers = {
        'User-Agent': 'bxchidao/0.1.0',
        'Authorization': 'Bearer %s' % u['outlook']['token'],
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    r = requests.get(graph('/me/events'),
                     headers=headers)

    return r.json()


def get_events_by_wxid_x(openid):
    u = mongo.db.users.find_one({'openid': openid})
    r = get_events_by_wxid(u)

    if 'error' in r:
        if r['error']['message'] == 'Access token has expired.':
            r = get_token('refresh_token', u['outlook']['refresh_token'])

            doc = mongo.db.users.find_one_and_update({
                'openid': openid
            }, {
                '$set': {
                    'outlook.refresh_token': r['refresh_token'],
                    'outlook.expires_on': r['expires_on'],
                    'outlook.token': r['access_token']
                }
            }, return_document=ReturnDocument.AFTER)

            r = get_events_by_wxid(doc)

    process_meeting_data(r, openid)
    return r
