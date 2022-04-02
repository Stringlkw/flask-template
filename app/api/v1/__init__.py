"""
@time: 2022/04/02
@file: __init__.py
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

from flask import Blueprint

from app.api.v1 import user, client, admin, image


def create_blueprint_v1():
    # 创建蓝图v1
    bp_v1 = Blueprint('v1', __name__)
    # 注册红图
    user.api.register(bp_v1)
    admin.api.register(bp_v1)
    client.api.register(bp_v1)
    image.api.register(bp_v1)

    return bp_v1
