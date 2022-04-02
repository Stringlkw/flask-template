"""
@time: 2022/04/02
@file: admin.py
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

from app.models.admin import Admin
from app.models.base import db
from app.models.user import User
from app.utils.enums import ClientTypeEnum
from app.utils.error_code import DeleteSuccess
from app.utils.redprint import Redprint
from app.utils.token import generate_auth_token
from app.utils.token_auth import auth
from app.validators.forms import ClientForm

# 定义红图
api = Redprint('admin')


# 管理员登录
@api.route('/login', methods=['POST'])
def login():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: Admin.verify,
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

    resp_dict = dict(code=200, msg="登录成功", data=data)
    return jsonify(resp_dict)


# 获取管理员信息
@api.route('/info', methods=['GET'])
@auth.login_required
def get_admin():
    uid = g.client.uid
    admin = Admin.query.filter_by(id=uid).first_or_404()
    resp_dict = dict(code=200, msg="获取管理员信息成功", data=admin)
    return jsonify(resp_dict)


# 管理员退出
@api.route('/logout', methods=['DELETE'])
@auth.login_required()
def logout():
    resp_dict = dict(code=200, msg="退出成功")
    return jsonify(resp_dict)


# 获取用户信息
@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    resp_dict = dict(code=200, msg="用户信息获取成功", data=user)
    return jsonify(resp_dict)


# 删除用户
@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()
