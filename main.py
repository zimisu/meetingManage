# -*-coding:utf-8-*-
__author__ = 'kanchan'
from app import app, TOKEN
from libs.constants import DEV
# from flask.ext.pymongo import PyMongo
from libs.oauth import *
from flask import request, session, render_template
import hashlib, json, requests
from sign import *
import pymongo


def flask_args_2_my_args(args):
    result = dict(args)
    for k in result:
        result[k] = args[k]
    return result


# 向微信服务器请求access_token
def request_access_token():
    print('----------------')
    print(cred)
    print('----------------')

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
          (cred['AppID'], cred['AppSecret'])
    return requests.get(url).json()['access_token']


# 获取缓存的access_token
def get_access_token():
    # todo: 储存缓存
    return request_access_token()


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
        print('weixin check successful!')
        return request.args['echostr']
    else:
        print('weixin check failed!')
        return 'failed!'


@app.route('/bind', methods=['POST'])
def bind():
    session['access_token'] = get_access_token()
    # 菜单栏事件，内含open_id
    if 'FromUserName' in request.form:
        session['openid'] = request.form['FromUserName']
    session['wx_user'] = request_wx_user()
    # todo: check again
    session['wx_user']['outlook'] = ''
    if mongo.db.users.find_one({'openid': session['openid']}) is None:
        mongo.db.users.insert(session['wx_user'])
    return ms_login()


@app.route('/check-in', methods=['POST'])
def check_in():
    meetingid = mongo.db.meeting_secret.find_one({'pic-secret': request.form['pic-secret']})
    # todo: 扫一扫怎么获取用户信息？
    openid = request.form['openid']
    try:
        if meetingid is not None:
            mongo.db.meeting.update_one({'meetingid': request.form['meetingid'],
                                         'attendee': {'openid': openid}},
                                        {'$set': {
                                            'attendee': {'status': 'checked'}
                                        }})
        else:
            return json.dumps({'result': 'failed',
                               'reason': 'Can not find a corresponding meeting.'})
    except pymongo.errors.PyMongoError:
        return json.dumps({'result': 'failed',
                           'reason': 'Error when insert into mongodb.'})


# todo: 是否有安全性问题？
@app.route('/app_args', methods=['GET'])
def get_app_args():
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % get_access_token()
    sign = Sign('jsapi_ticket', url).sign()
    sign['appId'] = cred['AppID']
    return json.dumps(sign)


@app.route('/check-in-scan', methods=['GET'])
def check_in_scan():
    return render_template('check-in-scan.html')


if __name__ == '__main__':
    # host = '0.0.0.0'
    host = '127.0.0.1'
    if DEV:
        app.run(debug=True, port=21667, host=host)
    else:
        app.run(debug=True, port=80, host='0.0.0.0')
