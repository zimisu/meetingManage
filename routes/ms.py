from pprint import pprint
import jwt
import requests
from pymongo import ReturnDocument

from app import app, mongo
import urllib.parse
from libs.constants import *
from libs.oauth import *
from flask import redirect, request


@app.route('/mslogin', methods=['GET'])
def ms_login():
    wx_uid = request.args.get('wx', '')

    oauth_params = urllib.parse.urlencode({
        'client_id': cred['client_id'],
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'state': wx_uid
    })
    return redirect(auth_endpoint_url % oauth_params)


@app.route('/cb', methods=['GET'])
def ms_login_cb():
    code = request.args.get('code', '')
    wx_uid = request.args.get('state', '')
    pprint(wx_uid)

    token_params = {
        'client_id': cred['client_id'],
        'client_secret': cred['secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'resource': RESOURCE
    }
    r = requests.post(token_endpoint_url, data=token_params)
    d = r.json()

    user_detail = jwt.decode(d['id_token'], verify=False)
    user_detail.update({
        'token': d['access_token'],
        'expires_on': d['expires_on'],
        'refresh_token': d['refresh_token']
    })

    _ = mongo.db.users.find_one_and_update({
        'openid': wx_uid
    }, {
        '$set': {
            'openid': wx_uid,
            'outlook': user_detail
        }
    }, upsert=True, return_document=ReturnDocument.AFTER)

    return '<html><head><title>已成功绑定账号</title></head>' \
           '<body>已成功绑定账号\n可以安全退出本页面</body></html>'

