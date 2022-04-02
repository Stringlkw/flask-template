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

from datetime import datetime

# import lib
from sqlalchemy import Column, String, Integer, DateTime, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base, db
from app.utils.error_code import AuthFailed

"""
管理员
    登录 /admin/login
    检查登陆状态 /admin/session
    登出 /admin/logout
    发送公告 /admin/bulletin/board
    获取登录日志 /admin/login/log
    获取操作日志 /admin/operate/log
    添加管理员 /admin/ manager
    删除管理员 /admin/ manager
    新增标签 /tag
    删除标签 /tag
    屏蔽用户 /user/status
    删除评论 /comment
    统计浏览量 /views/numbers
    查看所有用户略情 /all/user/int:page
    查看所有的反馈信息 /feedback/int:page"
    发博总数 /blog/numbers
    注册用户量 /register/numbers
    发表博客 /blog/article
    修改博客状态 /blog/article/status          
"""


# 管理员表
class Admin(Base):
    id = Column(Integer, primary_key=True)  # id号(独一无二的)
    email = Column(String(24), unique=True, nullable=False)
    username = Column(String(64), nullable=False, unique=True)  # 账号用户名
    _password = Column('password', String(256), nullable=False)
    avatar = Column(String(256), nullable=False)  # 头像
    auth = Column(SmallInteger, default=2)  # 权限(1: 超级管理员 2: 普通管理员)
    # onupdate 自动更新 每一次 增删查改这个表都会 自动更新一下时间
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 最近一次登录时间

    @staticmethod
    def keys():
        return ['id', 'email', 'username', 'avatar', 'auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(username, account, password, avatar):
        with db.auto_commit():
            admin = Admin()
            admin.username = username
            admin.email = account
            admin.password = password
            admin.avatar = avatar
            db.session.add(admin)

    @staticmethod
    def verify(email, password):
        user = Admin.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'SuperAdminScope' if user.auth == 1 else 'AdminScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self.password:
            return False
        return check_password_hash(self.password, raw)
