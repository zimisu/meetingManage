import hashlib
from urllib.parse import urljoin

from wechatpy import WeChatClient
from wechatpy.session.memcachedstorage import MemcachedStorage

from app import cred, app, TOKEN, mongo, mc

wx = WeChatClient(appid=cred['wx']['AppID'],
                  secret=cred['wx']['AppSecret'],
                  session=MemcachedStorage(mc))

from libs.constants import *


def wx_menu_init():
    wx.menu.create({
        'button': [{
            'type': 'click',
            'name': '绑定百姓账号',
            'key': WX_BTN_BIND_BX,
        }, {
            'type': 'click',
            'name': '开始签到',
            'key': WX_BTN_BEGIN_CHECKIN
        }, {
            'type': 'view',
            'name': '制定惩罚',
            'url': urljoin(DOMAIN, 'assign-punishment')
        }]
    })

