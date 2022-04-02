"""
@time: 2022/04/02
@file: user.py
@author: 李康伟                                    ┏┓      ┏┓
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

from flask import g, jsonify, current_app

from app.models.base import db
from app.models.user import User
from app.utils.enums import ClientTypeEnum
from app.utils.error_code import DeleteSuccess
from app.utils.redprint import Redprint
from app.utils.token import generate_auth_token
from app.utils.token_auth import auth
from app.validators.forms import ClientForm

api = Redprint('user')


# 用户登录
@api.route('/login', methods=['POST'])
def login():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.password.data
    )
    # 生成Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)

    data = {
        "token": token.decode('ascii')
    }

    resp_dict = dict(code=200, data=data)
    return jsonify(resp_dict), 200


# 获取用户信息
@api.route('/info', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.client.uid
    user = User.query.filter_by(id=uid).first_or_404()
    resp_dict = dict(code=200, data=user)
    return jsonify(resp_dict)


# 退出登录
@api.route('/logout', methods=['DELETE'])
@auth.login_required()
def logout():
    resp_dict = dict(code=200)
    return jsonify(resp_dict)


# 注销账号
@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.client.uid
    print(uid)
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()
