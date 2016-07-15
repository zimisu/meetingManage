from pprint import pformat
from urllib.parse import urljoin, urlencode

from flask import request
from wechatpy import parse_message
from wechatpy.events import ClickEvent, SubscribeScanEvent, ScanEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature
from libs.checkin import emit_checked_in

from app import app, TOKEN, mongo
from libs.constants import *
from libs.outlook.events import get_events_by_wxid_x
from libs.utility import check_in
# from libs.outlook.events import get_events_by_wxid_x
from libs.wx import wx


def all_attendees_checked(attendees):
    return len(list(map(lambda a: a['status'] == 'checked', attendees))) ==\
           len(attendees)


@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        _g = lambda k: request.args.get(k)

        try:
            print(TOKEN, _g('signature'), _g('timestamp'), _g('nonce'))
            check_signature(TOKEN,
                            _g('signature'),
                            _g('timestamp'),
                            _g('nonce'))

            return _g('echostr')
        except InvalidSignatureException:
            pass

    elif request.method == 'POST':
        msg = parse_message(request.data)

        if isinstance(msg, ClickEvent):
            ev = msg

            if ev.key == WX_BTN_BIND_BX:
                reply = TextReply()
                reply.source = ev.target
                reply.target = ev.source
                reply.content = '请访问以下链接登陆到BX邮箱\n%s' % (
                    '%s?%s' % (urljoin(DOMAIN, 'mslogin'),
                               urlencode({'wx': ev.source}))
                )
                return reply.render()
            elif ev.key == WX_BTN_BEGIN_CHECKIN:
                reply = TextReply()
                reply.source = msg.target
                reply.target = msg.source
                reply.content = '请访问以下链接选择开始哪个会议\n%s' % (
                    '%s/check-in-meetings?openid=%s' % (DOMAIN, msg.source)
                )
                return reply.render()
            else:
                reply = TextReply()
                reply.source = msg.target
                reply.target = msg.source
                reply.content = '哦'
                return reply.render()

        elif isinstance(msg, TextMessage):
            if msg.content.lower().startswith('e'):
                reply = TextReply()
                reply.source = msg.target
                reply.target = msg.source
                reply.content = '请访问以下链接选择开始哪个会议\n%s' % (
                    '%s/check-in-meetings?openid=%s' % (DOMAIN, msg.source)
                )

                return reply.render()
            else:
                return '哦'

        elif isinstance(msg, ScanEvent) or isinstance(msg, SubscribeScanEvent):
            openid = msg.source
            meetingid = msg.scene_id
            meeting = mongo.db.meeting.find_one({'meetingid': meetingid})
            ps = emit_checked_in(openid=openid, meeting=meeting)

            r = check_in(openid=openid, meetingid=meetingid, punish_str=ps)

            meeting = mongo.db.meeting.find_one({'meetingid': meetingid})
            if all_attendees_checked(meeting['attendee']):
                s = '签到汇总\n%s'
                ra = []
                for u in meeting['attendee']:
                    full_u = mongo.db.users.find_one({'openid': u['openid']})
                    ra.append([full_u['outlook']['name'],
                              meeting['attendee']['punish_str']])
                s %= '\n'.join(map(lambda ss: ': '.join(ss), ra))

                wx.message.send_mass_text(
                    map(lambda u: u['openid'], meeting['attendee']),
                    s, is_to_all=True)

            return r
