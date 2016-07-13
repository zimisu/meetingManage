from app import app, mongo
from libs.wx import wx
from flask import render_template, session
from flask import json
import traceback
import pymongo.errors

__author__ = 'kanchan'


def error_return(reason):
    return json.jsonify({'result': 'failed',
                         'reason': reason})


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return json.jsonify(request.args)
    else:
        return json.jsonify(request.form)


@app.route('/check-in', methods=['POST'])
def check_in():
    meetingid = mongo.db.meeting_secret.find_one({'pic-secret': request.form['pic-secret']})['meetingid']
    # todo: 扫一扫怎么获取用户信息？
    openid = request.form['openid']
    try:
        if meetingid is not None:
            mongo.db.meeting.update_one({'meetingid': request.form['meetingid'],
                                         'attendee': {'openid': openid}},
                                        {'$set': {
                                            'attendee': {'status': 'checked'}
                                        }})
            return json.jsonify({'result': 'ok'})
        else:
            return error_return('Can not find a corresponding meeting.')
    except pymongo.errors.PyMongoError:
        traceback.print_exc()
        reason = 'check_in(): Error when update mongodb in check_in().'
        print(reason)
        return error_return(reason)
    except:
        traceback.print_exc()
        return error_return('Other exception')


@app.route('/meeting/', methods=['GET'])
@app.route('/meeting/<meetingid>', methods=['GET'])
def meeting(meetingid=None):
    # todo: get openid
    openid = ''
    if mongo.db.users.find({'openid': openid}).count() == 0:
        print('openid: %s is not in mongodb.Should bind first.')
        return error_return('该用户未绑定百姓网账号，请先绑定')
    try:
        if meetingid is not None:
            # todo: 带入用户信息. check it again
            ret = mongo.db.meeting.find_one({'meetingid': meetingid,
                                             'attendee.openid': openid})
            wx_user = json.loads(wx.user.get(openid))
            for i in range(len(ret['attendee'])):
                ret['attendee'][i].update(wx_user)
            ret['result'] = 'ok'
            return json.jsonify(ret)
        else:
            # todo: check it again. 是否需要带入用户信息？
            ret = {'result': 'ok',
                   'meetings': mongo.db.meeting.find({'attendee.openid': openid})}
            return ret
    except pymongo.errors.PyMongoError:
        traceback.print_exc()
        reason = 'meeting(): Error exists when get meeting in mongo.'
        print(reason)
        return error_return(reason)
    except:
        traceback.print_exc()
        reason = 'meeting(): Other error exists when get meeting.'
        print(reason)
        return error_return(reason)


@app.route('/punishments', methods=['GET'])
def punishments():
    try:
        ret = {'punishments': mongo.db.punishments.find(),
               'result': 'ok'}
        return ret
    except:
        traceback.print_exc()
        reason = 'punishments(): Error exists when get punishments'
        print(reason)
        return error_return(reason)


@app.route('/add_punishment', methods=['POST'])
def add_punishment():
    try:
        item = {'ptype': int(request.form['ptype']),
                'content': request.form['content']}
        mongo.db.punishments.insert_one(item)
        return json.jsonify({'result': 'ok'})
    except:
        traceback.print_exc()
        reason = 'add_punishment(): Error exists when add punishment'
        print(reason)
        return error_return(reason)


@app.route('/app_args', methods=['GET'])
def get_app_args():
    return 'This url should not be used!'
    # result = wx.jsapi.get_jsapi_ticket()
    #
    # ret = {
    #     'appId': cred['wx']['AppID']
    # }
    #
    # result['appId'] = cred['wx']['AppID']
    # return result


@app.route('/check-in-scan', methods=['GET'])
def check_in_scan():
    return render_template('check-in-scan.html')


from routes.ms import *
from routes.wx import *

if __name__ == '__main__':
    # host = '0.0.0.0'
    host = '127.0.0.1'

    DEV = False

    if DEV:
        app.run(debug=True, port=21667, host=host)
    else:
        app.run(debug=True, port=80, host='0.0.0.0')
