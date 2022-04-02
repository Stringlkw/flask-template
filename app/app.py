"""
@time: 2022/04/02
@file: app.py
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

from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.config.secure import config_map
from app.utils.error_code import ServerError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d-%H:%M:%S')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1())


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)


def create_app(dev_name):
    """
    返回一个实例化并且配置好数据的一个app
    dev_name：选择环境的参数
    :return:
    """
    app = Flask(__name__)
    config_class = config_map.get(dev_name)
    app.config.from_object(config_class)  # 从类中读取需要的信息
    app.config.from_object('app.config.setting')
    register_blueprints(app)
    register_plugin(app)
    return app
