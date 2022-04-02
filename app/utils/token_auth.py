"""
@time: 2022/04/02
@file: token_auth.py
@author:李康伟                                     ┏┓      ┏┓
@contact: 1005446851@qq.com                     ┏┛┻━━━┛┻┓
@license: Apache Licence                        ┃      ☃      ┃
                                                ┃  ┳┛  ┗┳  ┃
                                                ┃      ┻      ┃
                                                ┗━┓      ┏━┛
                                                    ┃      ┗━━━┓
                                                    ┃  神兽保佑    ┣┓
                                                    ┃　永无BUG！   ┏┛
                                                    ┗┓┓┏━┳┓┏┛
                                                      ┃┫┫  ┃┫┫
                                                      ┗┻┛  ┗┻┛
"""

from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.utils.error_code import AuthFailed, Forbidden
from app.utils.scope import is_in_scope

auth = HTTPBasicAuth()
Client = namedtuple('Client', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(_, __):
    token = request.headers.get('token')
    client_info = verify_auth_token(token)

    if not client_info:
        return False
    else:
        g.client = client_info
    return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        # token无效
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        # token过期
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return Client(uid, ac_type, scope)
