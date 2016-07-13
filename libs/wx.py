import hashlib
from urllib.parse import urljoin

from wechatpy import WeChatClient

from app import cred, app, TOKEN

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
        }]
    })


def flask_args_2_my_args(args):
    result = dict(args)
    for k in result:
        result[k] = args[k]
    return result


def check_from_wechat(args):
        if 'signature' in args and 'timestamp' in args and 'nonce' in args and 'echostr' in args:
            print (''.join(sorted([args['timestamp'],
                                   args['nonce'],
                                   TOKEN])))
            sign = hashlib.sha1(''.join(sorted([args['timestamp'],
                                                args['nonce'],
                                                TOKEN])))
            print('sign: ' + sign.hexdigest())
            print('signature: ' + args['signature'])
            if sign.hexdigest() == args['signature']:
                return True
        return False
