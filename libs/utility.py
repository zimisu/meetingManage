# -*-coding:utf-8-*-
__author__ = 'kanchan'

from app import mongo
import pymongo
import traceback
from flask import json
import time
from libs.constants import TIME_FORMAT


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


def check_in(openid, meetingid):
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
                    return '已经签到啦，不用重复签到'
                else:
                    print('update')
                    user(i)['status'] = 'checked'
                    user(i)['timestamp'] = time.time()
                    mongo.db.meeting.update_one({'meetingid': meetingid},
                                                {'$set': m})
                    print('check-in successful!!!')
                    return '签到成功！'
    except pymongo.errors.PyMongoError:
        traceback.print_exc()
        reason = 'check_in(): Error when update mongodb in check_in().'
        print(reason)
        return error_return(reason)
    except:
        traceback.print_exc()
        return error_return('Other exception')
