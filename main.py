# -*-coding:utf-8-*-
__author__ = 'kanchan'
from app import app, mongo
from libs.wx import wx
from flask import render_template
import json
import pymongo.errors


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return json.dumps(request.args)
    else:
        return json.dumps(request.form)


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
            return json.dumps({'result': 'ok'})
        else:
            return json.dumps({'result': 'failed',
                               'reason': 'Can not find a corresponding meeting.'})
    except pymongo.errors.PyMongoError:
        return json.dumps({'result': 'failed',
                           'reason': 'Error when insert into mongodb.'})


@app.route('/meeting', methods=['GET'])
def meeting():
    try:
        m = mongo.db.meeting.find_one({'meetingid': request.args.get('meetingid')})
        m['result'] = 'ok'
        return json.dumps(m)
    except Exception:
        print('get meeting information error.')
        return json.dumps({'result': 'failed',
                           'reason': ''})


@app.route('/app_args', methods=['GET'])
def get_app_args():
    return wx.jsapi.get_jsapi_ticket()


@app.route('/check-in-scan', methods=['GET'])
def check_in_scan():
    return render_template('check-in-scan.html')


from routes.ms import *
from routes.wx import *


if __name__ == '__main__':
    # host = '0.0.0.0'
    host = '127.0.0.1'
    if DEV:
        app.run(debug=True, port=21667, host=host)
    else:
        app.run(debug=True, port=80, host='0.0.0.0')
