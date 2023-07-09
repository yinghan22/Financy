"""
@file    : Redis.py
@author  : yingHan/嬴寒
@email   : yinghan22@163.com
@create  : 2023/04/09 14:43
"""
from sanic import Sanic
from sanic_redis import SanicRedis


def register_redis(app: Sanic = None, config_name: str = 'REDIS', redis_url: str = 'redis://localhost:6379/0'):
    app.config.update({
        config_name: redis_url
    })
    SanicRedis(
        app=app,
        config_name=config_name,
        redis_url=redis_url
    )
