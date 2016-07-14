from math import floor

from libs.wx import wx
from app import sio, mongo


def emit_checked_in(openid, meeting):
    user = wx.user.get(openid)
    sio.emit('check-in', user)

    checkin_time = meeting['attendee']['openid']['time']
    if checkin_time > meeting['time']:
        chidao = (checkin_time - meeting['time']).total_seconds / 60

        punishment = ''
        p_obj = mongo.db.punishments.find_one({
            'punishment_id': meeting['punishment_id']
        })
        if p_obj['ptype'] == 1:
            every, kuai = p_obj['content']
            num = floor(chidao / every) * kuai
            punishment = '%f块钱' % (num)
        elif p_obj['ptype'] == 2:
            every, amount, unit = p_obj['content']
            num = floor(chidao / every) * amount
            punishment = '%f%s' % (num, unit)
        else:
            text, = p_obj['content']
            punishment = text

        wx.message.send_text(openid, '你已迟到%d分钟, 惩罚是%s' % (
            chidao,
            punishment
        ))
    else:
        wx.message.send_text(openid, '签到成功')
