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

from datetime import datetime

# import lib
from sqlalchemy import Column, String, Integer, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base, db
from app.utils.error_code import AuthFailed


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    username = Column(String(24), unique=True)
    _password = Column('password', String(256), nullable=False)
    avatar = Column(String(256), nullable=False,
                    default='https://pic3.zhimg.com/80/v2-6ba00ea444a8ccee72cac94995e68dcc_720w.jpg?source=1940ef5c')  # 头像
    # onupdate 自动更新 每一次 增删查改这个表都会 自动更新一下时间
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 最近一次登录时间

    @staticmethod
    def keys():
        return ['id', 'email', 'username', 'avatar']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(username, account, password, avatar):
        with db.auto_commit():
            user = User()
            user.username = username
            user.email = account
            user.password = password
            user.avatar = avatar
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self.password:
            return False
        return check_password_hash(self.password, raw)
