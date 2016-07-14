from app import app, mongo, sio
from libs.wx import wx
from flask import render_template, session
from flask import json
import traceback
import pymongo.errors
from libs.utility import error_return
from datetime import datetime

__author__ = 'kanchan'


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return json.jsonify(request.args)
    else:
        return json.jsonify(request.form)


@app.route('/new-qr-code/<meetingid>', methods=['GET'])
def new_qr_code(meetingid):
    # todo: uncompleted
    # res = {"ticket": string, "expire_seconds": int, "url":qr-pic-url}
    res = wx.qrcode.create({
        'expire_seconds': 36000,
        'action_name': 'QR_SCENE',
        'action_info': {
            'scene': {'scene_id': meetingid}
        }
    })
    return json.jsonify({'url': wx.qrcode.get_url(res['ticket']), 'result': 'ok'})


@app.route('/check-in', methods=['POST'])
def check_in():
    meetingid = mongo.db.meeting_secret.find_one({'pic-secret': request.form['pic-secret']})['meetingid']
    # todo: 扫一扫怎么获取用户信息？
    openid = request.form['openid']
    try:
        if meetingid is not None:
            tmp = mongo.db.meeting.find_one({'meetingid': request.form['meetingid'],
                                             'attendee': {'openid': openid}},
                                            {'_id': 0})
            # check whether the attendee had checked
            for user in tmp['attendee']:
                if user['openid'] == openid:
                    if user['status'] == 'checked':
                        return error_return('checked')
                    break
            mongo.db.meeting.update_one({'meetingid': request.form['meetingid'],
                                         'attendee.openid': openid},
                                        {'$set': {'attendee.status': 'checked',
                                                  'attendee.time': datetime.now().timestamp()}})
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


@app.route('/meeting', methods=['GET'])
@app.route('/meeting/', methods=['GET'])
@app.route('/meeting/<meetingid>', methods=['GET'])
def meeting(meetingid=None):
    openid = request.args.get('openid', '')
    try:
        if meetingid is None:
            if mongo.db.users.find({'openid': openid}).count() == 0:
                print('openid: %s is not in mongodb.Should bind first.' % openid)
                return error_return('该用户未绑定百姓网账号，请先绑定')
            get_events_by_wxid_x(openid)

            ret = {'result': 'ok',
                   'meetings': [i for i in mongo.db.meeting.find({'attendee.openid': openid}, {'_id': 0})]}
            return json.jsonify(ret)
        else:
            ret = mongo.db.meeting.find_one({'meetingid': meetingid}, {'_id': 0})
            for i in range(len(ret['attendee'])):
                if ret['attendee'][i]['openid'] != '':
                    wx_user = wx.user.get(ret['attendee'][i]['openid'])
                    ret['attendee'][i].update(wx_user)
            ret['result'] = 'ok'
            return json.jsonify(ret)
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
        ret = {'punishments': [i for i in mongo.db.punishments.find({}, {'_id': 0})],
               'result': 'ok'}
        return json.jsonify(ret)
    except:
        traceback.print_exc()
        reason = 'punishments(): Error exists when get punishments'
        print(reason)
        return error_return(reason)


@app.route('/add_punishment', methods=['POST'])
def add_punishment():
    try:
        item = request.form.to_dict()
        tmp = {'ptype': item['ptype'],
               'content': [1] * (len(item) - 1)}
        print(item)
        for i in range(len(item) - 1):
            tmp['content'][i] = item['content' + str(i)]
        tmp['punishment_id'] = mongo.db.punishments.find().count()
        mongo.db.punishments.insert_one(tmp)
        return json.jsonify({'result': 'ok'})
    except:
        traceback.print_exc()
        reason = 'add_punishment(): Error exists when add punishment'
        print(reason)
        return error_return(reason)


@app.route('/bind_meeting_punishment', methods=['POST'])
def bind_meeting_punishment():
    try:
        meetingid = request.args['meetingid']
        punishment_id = request.args['punishment_id']
        mongo.db.meeting.update({'meetingid': meetingid},
                                {'punishment_id': punishment_id})
        return json.jsonify({'result': 'ok'})
    except pymongo.errors.PyMongoError:
        traceback.print_exc()
        reason = 'bind_meeting_punishment(): Error exists when bind punishment to meeting.'
        print(reason)
        return error_return(reason)
    except:
        traceback.print_exc()
        reason = 'bind_meeting_punishment(): Other error exists.'
        print(reason)
        return error_return(reason)


@app.route('/attendee', methods=['GET'])
def attendee():
    try:
        meetingid = request.args['meetingid']
        openid = request.args['openid']
        m = mongo.db.meeting.find_one({'meetingid': meetingid})
        if m is None:
            return error_return('Could not find the meeting')
        for user in m['attendee']:
            if user['openid'] == openid:
                ret = user
                ret['result'] = 'ok'
                return json.jsonify(ret)
        return error_return('Could not find the attendee')
    except pymongo.errors.PyMongoError:
        traceback.print_exc()
        reason = 'attendee(): Error exists when query attendee from mongo db.'
        print(reason)
        return error_return(reason)
    except:
        traceback.print_exc()
        reason = 'attendee(): Other error exists.'
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
@app.route('/check-in-scan.html', methods=['GET'])
def check_in_scan():
    return render_template('check-in-scan.html')


@app.route('/assign-punishment', methods=['GET'])
@app.route('/assign-punishment.html', methods=['GET'])
def assign_punishment():
    return render_template('assign-punishment.html')


@app.route('/punishments_', methods=['GET'])
@app.route('/punishments.html', methods=['GET'])
def punishments_html():
    return render_template('punishments.html')


@app.route('/add-punishment_', methods=['GET'])
@app.route('/add-punishment.html', methods=['GET'])
def add_punishment_html():
    return render_template('add-punishment.html')


@app.route('/show-QR-code', methods=['GET'])
@app.route('/show-QR-code.html', methods=['GET'])
def show_qr_code_html():
    return render_template('show-QR-code.html')


@app.route('/check-in-members', methods=['GET'])
@app.route('/check-in-members.html', methods=['GET'])
def check_in_members():
    return render_template('check-in-members.html')


@app.route('/check-in-meetings', methods=['GET'])
@app.route('/check-in-meetings.html', methods=['GET'])
def check_in_meetings():
    return render_template('check-in-meetings.html')


from routes.ms import *
from routes.wx import *

if __name__ == '__main__':
    # host = '0.0.0.0'
    host = '127.0.0.1'

    DEV = False

    if DEV:
        sio.run(app, debug=True, port=21667, host=host)
    else:
        sio.run(app, debug=False, port=80, host='0.0.0.0')
