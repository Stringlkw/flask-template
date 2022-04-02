"""
@time: 2022/04/02
@file: secure.py 
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


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "632547"
    TOKEN_EXPIRATION = 30 * 24 * 3600  # token数据的有效期，单位秒


# 开发环境
class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/sar'
    DEBUG = True


# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jamkung@pukgai.com:3306/caiji_pro'


config_map = {
    "development": DevelopmentConfig,
    "product": ProductionConfig
}
