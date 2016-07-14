import hashlib
from urllib.parse import urljoin

from wechatpy import WeChatClient

from app import cred, app, TOKEN, mongo

wx = WeChatClient(appid=cred['wx']['AppID'],
                  secret=cred['wx']['AppSecret'])

from libs.constants import *


def wx_menu_init():
    wx.menu.create({
        'button': [{
            'type': 'click',
            'name': '绑定百姓账号',
            'key': WX_BTN_BIND_BX,
            'url': urljoin(DOMAIN, 'bind')
        }, {
            'type': 'click',
            'name': '开始签到',
            'key': WX_BTN_BEGIN_CHECKIN
        }, {
            'type': 'click',
            'name': '签到',
            'key': WX_BTN_CHECKIN
        }]
    })

