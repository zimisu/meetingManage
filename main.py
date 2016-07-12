# -*-coding:utf-8-*-
__author__ = 'kanchan'

# from flask.ext.pymongo import PyMongo
from flask import request, Flask
import json, hashlib

app = Flask(__name__)
TOKEN = 'baixingg5'


# mongo = PyMongo(app)

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
            if sign.hexdigest() == request.args['signature']:
                return True
        return False


@app.route('/test', methods=['POST', 'GET'])
def test():
    return request.args.items().__str__()


@app.route('/weixin', methods=['GET'])
def weixin():
    if check_from_wechat(request.args):
        print('wexin check successful!')
        return request.args['echostr']
    else:
        print('wexin check failed!')
        return 'failed!'


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
