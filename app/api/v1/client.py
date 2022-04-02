"""
@time: 2022/04/02
@file: client.py
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

from app.models.admin import Admin
from app.models.user import User
from app.utils.enums import ClientTypeEnum
from app.utils.error_code import Success
from app.utils.redprint import Redprint
from app.validators.forms import ClientForm, UserEmailForm, AdminEmailForm

api = Redprint('client')


# 管理员注册
@api.route('/admin/register', methods=['POST'])
def create_admin():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_admin_by_email
    }
    promise[form.type.data]()
    return Success(msg='注册成功')


def __register_admin_by_email():
    form = AdminEmailForm().validate_for_api()
    Admin.register_by_email(form.username.data, form.account.data, form.password.data, form.avatar.data)


# 用户注册
@api.route('/user/register', methods=['POST'])
def create_user():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success(msg='注册成功')


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.username.data, form.account.data, form.password.data, form.avatar.data)
