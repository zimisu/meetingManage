from urllib.parse import urljoin

import requests
from flask import request
from wechatpy import parse_message
from wechatpy.events import ClickEvent
from wechatpy.replies import TextReply

from app import app
from libs.constants import *
from libs.wx import check_from_wechat, wx_menu_init


wx_menu_init()


@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        if check_from_wechat(request.args):
            print('wexin check successful!')
            return request.args['echostr']
        else:
            print('wexin check failed!')
            return 'failed!'

    elif request.method == 'POST':
        msg = parse_message(request.data)
        if isinstance(msg, ClickEvent):
            ev = msg
            if ev.key == WX_BTN_BIND_BX:
                reply = TextReply()
                reply.source = ev.target
                reply.target = ev.source
                reply.content = '请访问以下链接登陆到BX邮箱\n%s' % (
                    requests.get(urljoin(DOMAIN, 'mslogin'), params={
                        'wx': ev.source
                    }).url
                )
                return reply.render()
