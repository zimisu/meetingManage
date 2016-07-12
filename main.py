# -*-coding:utf-8-*-
__author__ = 'kanchan'

from app import app, TOKEN
from libs.constants import DEV
# from flask.ext.pymongo import PyMongo
from libs.oauth import *
from flask import request, session
import hashlib
import json
import requests


def flask_args_2_my_args(args):
    result = dict(args)
    for k in result:
        result[k] = args[k]
    return result


def request_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
          (cred['wx']['AppID'], cred['wx']['AppSecret'])
    return requests.get(url).json()['access_token']


def request_wx_user():
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s' % \
          (session['access_token'], session['openid'])
    return requests.get(url).json()

def check_from_wechat(args):
    if 'signature' in args and 'timestamp' in args and 'nonce' in args and 'echostr' in args:
        print(''.join(sorted([args['timestamp'],
                              args['nonce'],
                              TOKEN])))
        sign = hashlib.sha1(''.join(sorted([args['timestamp'],
                                            args['nonce'],
                                            TOKEN])))
        print('sign: ' + sign.hexdigest())
        print('signature: ' + args['signature'])
        if sign.hexdigest() == request.args['signature']:
            return True
    return False


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return json.dumps(request.args)
    else:
        return json.dumps(request.form)


@app.route('/weixin', methods=['GET'])
def weixin():
    if check_from_wechat(request.args):
        print('wexin check successful!')
        return request.args['echostr']
    else:
        print('wexin check failed!')
        return 'failed!'


@app.route('/bind', methods=['POST'])
def bind():
    session['access_token'] = request_access_token()
    # 菜单栏事件，内含open_id
    if 'FromUserName' in request.form:
        session['openid'] = request.form['FromUserName']
    session['wx_user'] = request_wx_user()
    # todo: check again
    session['wx_user']['outlook'] = ''
    mongo.db.users.insert(session['wx_user'])
    return ms_login()


if __name__ == '__main__':
    # host = '0.0.0.0'
    host = '127.0.0.1'
    if DEV:
        app.run(debug=True, port=21667, host=host)
    else:
        app.run(port=80, host='0.0.0.0')
