from pprint import pprint
import jwt
import requests

from app import app, cred
import urllib.parse
from libs.constants import *
from libs.oauth import *
from flask import redirect, request, session


@app.route('/mslogin', methods=['GET'])
def ms_login():
    wx_uid = request.args.get('wx', '')
    session['wx'] = wx_uid

    oauth_params = urllib.parse.urlencode({
        'client_id': cred['client_id'],
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
    })
    return redirect(auth_endpoint_url % oauth_params)


@app.route('/cb', methods=['GET'])
def ms_login_cb():
    code = request.args.get('code', '')

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

    pprint(d)

    user_detail = jwt.decode(d['id_token'], verify=False)
    user_detail.update({
        'token': d['access_token'],
        'expires_on': d['expires_on'],
        'refresh_token': d['refresh_token']
    })
    pprint(user_detail)

    pprint(session)
    # wxu = session['wx_user']
    # mongo.db.users.find_one_and_update({
    #     '_id': wxu['_id']
    # }, {
    #     'outlook': user_detail
    # })

    return str(d)

