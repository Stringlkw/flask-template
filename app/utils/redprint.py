"""
@time: 2022/04/02
@file: redprint.py
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


class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
