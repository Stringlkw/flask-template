"""
@time: 2022/04/02
@file: form.py
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

from wtforms import StringField, IntegerField
from wtforms import ValidationError
from wtforms.validators import DataRequired, length, Email, Regexp

from app.models.admin import Admin
from app.models.user import User
from app.utils.enums import ClientTypeEnum
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(min=5, max=32)])
    password = StringField()
    type = IntegerField(validators=[DataRequired()])
    avatar = StringField()

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    password = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    username = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    @staticmethod
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message="邮箱已被注册")

    @staticmethod
    def validate_username(self, value):
        if User.query.filter_by(username=value.data).first():
            raise ValidationError(message="用户名已被注册")


class AdminEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    password = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    username = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    @staticmethod
    def validate_account(self, value):
        if Admin.query.filter_by(email=value.data).first():
            raise ValidationError(message="邮箱已被注册")
