import urllib.parse

import requests

from app import app, cred
from flask import redirect, request
from libs.constants import DOMAIN


auth_endpoint_url = 'https://login.chinacloudapi.cn/%s/oauth2/authorize?%%s' % cred['tenant']
token_endpoint_url = 'https://https://login.chinacloudapi.cn/%s/oauth2/token' % cred['tenant']

REDIRECT_URI = '/'.join([DOMAIN, 'cb'])


@app.route('/mslogin', methods=['GET'])
def ms_login():
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
        'resource': DOMAIN
    }
    r = requests.post(token_endpoint_url, data=token_params)
    d = r.json()

    return str(d)
