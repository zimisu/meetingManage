import requests

from app import cred
from libs.constants import REDIRECT_URI, RESOURCE

auth_endpoint_url = 'https://login.chinacloudapi.cn/%s/oauth2/authorize?%%s' % cred['tenant']
token_endpoint_url = 'https://login.chinacloudapi.cn/%s/oauth2/token' % cred['tenant']


def get_token(grant_type, code):
    token_params = {
        'client_id': cred['client_id'],
        'client_secret': cred['secret'],
        'grant_type': grant_type,
        'redirect_uri': REDIRECT_URI,
        'resource': RESOURCE
    }
    if grant_type == 'authorization_code':
        token_params['code'] = code
    elif grant_type == 'refresh_token':
        token_params['refresh_token'] = code

    return requests.post(token_endpoint_url, data=token_params).json()
