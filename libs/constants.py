DOMAIN = 'http://bxchidao.qwert42.org'

DEV = True


WX_BTN_BIND_BX = 'bind_bx'
WX_BTN_BEGIN_CHECKIN = 'begin_checkin'
WX_BTN_CHECKIN = 'checkin'


REDIRECT_URI = '/'.join([DOMAIN, 'cb'])
# REDIRECT_URI = 'http://127.0.0.1:21569/cb'

RESOURCE = 'https://microsoftgraph.chinacloudapi.cn'
GRAPH_EP = '%s/v1.0' % RESOURCE
