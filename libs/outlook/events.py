from collections import OrderedDict
from pprint import pprint
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import requests
from pymongo import ReturnDocument

from app import mongo
from libs.constants import GRAPH_EP
from libs.oauth import get_token


def get_events_by_wxid(u):
    headers = OrderedDict([
        # ('User-Agent', 'bxchidao/0.1.0'),
        ('Authorization', 'Bearer %s' % u['outlook']['token']),
        ('Accept', 'application/json'),
        ('Content-Type', 'application/json')
    ])

    url = 'me/events'
    url = '/'.join((GRAPH_EP, url))
    # req = Request(url, headers=headers)
    r = requests.get('/'.join((GRAPH_EP, url)),
                     headers=headers)
    print(r.url)
    return r


def get_events_by_wxid_x(mongo, openid):
    u = mongo.users.find_one({'openid': openid})

    r = get_events_by_wxid(u)

    print(r)
    if 'odata.error' in r:
        if True: # r['odata.error']['code'] == 'Authentication_ExpiredToken':
            r = get_token('refresh_token', u['outlook']['refresh_token'])
            pprint(r)

            doc = mongo.users.find_one_and_update({
                'openid': openid
            }, {
                '$set': {
                    'outlook.refresh_token': r['refresh_token'],
                    'outlook.expires_on': r['expires_on'],
                    'outlook.token': r['access_token']
                }
            }, return_document=ReturnDocument.AFTER)
            pprint(doc)

            r = get_events_by_wxid(doc)
            pprint(r)
            return r
    else:
        return r

