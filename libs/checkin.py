from libs.wx import wx
from app import sio


def emit_checked_in(openid):
    user = wx.user.get(openid)
    sio.emit('check-in', user)
