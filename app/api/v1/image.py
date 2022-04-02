"""
@time: 2022/04/02
@file: image.py
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

from flask import Response

from app.utils.redprint import Redprint

api = Redprint('image')


# 获取图片
@api.route('/<image_name>', methods=['GET'])
def get_image(image_name):
    with open(f'./app/image/{image_name}', 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype='image')
        return resp
