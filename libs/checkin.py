from math import floor

from libs.wx import wx
from app import sio, mongo
import datetime as dt


def emit_checked_in(openid, meeting):
    user = wx.user.get(openid)
    sio.emit('check-in', user)

    for user in meeting['attendee']:
        if user['openid'] != openid:
            continue

        checkin_time = dt.datetime.now().timestamp()
        print('--------')
        print(checkin_time)
        print(meeting['timestamp'])
        if checkin_time > meeting['timestamp']:
            chidao = (checkin_time - meeting['timestamp']) / 60

            p_obj = mongo.db.punishments.find_one({
                'punishment_id': meeting['punishment_id']
            })
            if p_obj['ptype'] == 1 or p_obj['ptype'] == '1':
                every, kuai = p_obj['content']
                num = floor(chidao / float(every)) * float(kuai)
                punishment = '%f块钱' % (num)
            elif p_obj['ptype'] == 2 or p_obj['ptype'] == '2':
                every, amount, unit = p_obj['content']
                num = floor(chidao / float(every)) * float(amount)
                punishment = '%f%s' % (num, unit)
            else:
                print(p_obj['content'])
                text, = p_obj['content']
                punishment = text

            s = '你已迟到%d分钟, 惩罚是%s' % (
                chidao,
                punishment
            )
            # wx.message.send_text(openid, s)

            return [checkin_time, s]
        else:
            # wx.message.send_text(openid, '签到成功')
            return [checkin_time, '没有迟到，不用惩罚~']
