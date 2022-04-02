"""
@time: 2022/04/02
@file: manage.py
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

from flask_cors import CORS
from flask_migrate import Migrate  # 管理数据库需要的脚本 追踪数据库变化的脚本
# import lib
from werkzeug.exceptions import HTTPException

from app.app import create_app
from app.models.base import db
from app.utils.error import APIException
from app.utils.error_code import ServerError

app = create_app("development")
CORS(app, supports_credentials=True)
Migrate(app, db)  # 把app和db的信息绑定起来进行追踪

"""
flask db init #初始化
flask db migrate -m "init message" #提交变更
flask db upgrade # 升级变更
flask db downgrade # 降级变更
"""


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 是否处于调试模式
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run()
