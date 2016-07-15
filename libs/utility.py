# -*-coding:utf-8-*-
__author__ = 'kanchan'

from app import mongo
import pymongo
import traceback
from flask import json
import time
from libs.constants import TIME_FORMAT
from libs.wx import wx


def error_return(reason):
    return json.jsonify({'result': 'failed',
                         'reason': reason})


def get_timestamp(string=None):
    if string is None:
        return time.time()
    else:
        return time.mktime(time.strptime(string, TIME_FORMAT))


def get_strtime(t=None):
    if t is None:
        return time.strftime(TIME_FORMAT)
    else:
        return time.strftime(TIME_FORMAT, time.localtime(time.time()))


def check_in(openid, meetingid, punish_str=None):
    try:
        print(openid)
        print(meetingid)
        meetingid = str(meetingid)
        m = mongo.db.meeting.find_one({'meetingid': meetingid})
        mongo.db.meeting.find_one({'meetingid': meetingid,
                                   'attendee.openid': openid})
        if m is None:
            print('The user doesn''t take part in this meeting')
            return error_return('该用户没有参加该会议')
        print(m)
        for i in range(len(m['attendee'])):
            user = lambda k: m['attendee'][k]
            if user(i)['openid'] == openid:
                if user(i)['status'] == 'checked':
                    print('This user doesn''t need to check in')
                    # return '已经签到啦，不用重复签到'
                    wx.message.send_text(openid, '已经签到啦，不用重复签到')
                else:
                    print('update')
                    user(i)['status'] = 'checked'
                    user(i)['timestamp'] = time.time()
                    if punish_str is not None:
                        user(i)['punish_str'] = punish_str
                    else:
                        user(i)['punish_str'] = '没有惩罚 T.T'
                    mongo.db.meeting.update_one({'meetingid': meetingid},
                                                {'$set': m})
                    print('check-in successful!!!')
                    wx.message.send_text(openid, '签到成功！')
                    # return '签到成功！'
    except pymongo.errors.PyMongoError:
        traceback.print_exc()
        reason = 'check_in(): Error when update mongodb in check_in().'
        print(reason)
        return error_return(reason)
    except:
        traceback.print_exc()
        return error_return('Other exception')


def create_attendee(man):
    attendee = {'email': man['emailAddress']['address'],
                'status': 'not checked',
                'timestamp': 0,
                'openid': ''}
    tmp = mongo.db.users.find_one({'outlook.upn': attendee['email']})
    if tmp is not None:
        attendee['openid'] = tmp['openid']
    return attendee


def insert_meeting_data(m):
    if mongo.db.meeting.find_one({'id': m['id']}) is not None:
        return
    print('begin to insert meeting')
    t = m['start']['dateTime']
    t = t[:t.find('.')]
    result = {
        # todo: meetingid
        'meetingid': str(mongo.db.meeting.find().count()),
        'timestamp': time.mktime(time.strptime(t, '%Y-%m-%dT%H:%M:%S')),
        'id': m['id'],
        'title': m['subject'],
        'content': m['bodyPreview'],
        'place': m['location']['displayName'],
        'start': 0,
        'punishment_id': 0,
        'organizer': create_attendee(m['organizer']),
        'attendee': []
    }
    for man in m['attendees']:
        result['attendee'].append(create_attendee(man))
    mongo.db.meeting.insert(result)


def process_meeting_data(data):
    # print('---------***-------')
    # for k in data:
    #     print(k)
    # print('---------***-------')
    for m in data['value']:
        insert_meeting_data(m)
