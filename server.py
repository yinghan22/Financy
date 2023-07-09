import traceback

from sanic import Sanic
from sanic_cors import CORS
from tortoise.contrib.sanic import register_tortoise

from Config import Config
from utils.AutoLoad import autodiscover
from utils.Redis import register_redis
from utils.Response import Response

app = Sanic(name='financySystem')

register_tortoise(
    app,
    db_url=Config['db_server'],
    modules={'models': ['models']},
    generate_schemas=True,
)

register_redis(app, redis_url=Config['redis_server'])

autodiscover(
    app,
    'modules',
    recursive=True,
)

CORS(app)


@app.route('/api/test')
async def test(request):
    return Response().success()


@app.exception(Exception)
async def handle_exception(request, exception):
    tb = traceback.extract_tb(exception.__traceback__)[-1]
    message = f"异常:{tb.filename}:{tb.lineno}:{tb.name}> {tb.line}. 异常信息: {str(exception)}."
    return Response().error(message=message)


# @app.middleware('request')
# async def auth_middleware(request):
#     if request.path != '/user/login':
#         token = request.headers.get('X-token', '')
#         async with request.app.ctx.redis as redis:
#             temp = await redis.get(f"token:{token}")
#             if temp is None:
#                 return Response().error(message='请重新登录')
#             else:
#                 await redis.set(f"token:{token}", token, ex=Config['time']['three_day'])
#             id = request.cookies.get('id', '').strip()
#             token = request.cookies.get('token', '').strip()
#             if id == '' or token == '':
#                 return Response().error(message='请重新登录')
#             __token__ = json.loads(await redis.hget('token', id))
#             if token != __token__:
#                 return Response().error(message='请重新登录')


# @app.middleware('response')
# async def session_middleware(request, response):
#     if request.path not in ['/user/login', '/user/logout']:
#         token = request.headers.get('X-token', '')
#         async with request.app.ctx.redis as redis:
#             temp = await redis.get(f"token:{token}")
#             if temp is None:
#                 return Response().error(message='请重新登录')
#             else:
#                 await redis.set(f"token:{token}", token, ex=Config['time']['three_day'])
#                 response.headers.set('X-token', token)
#
#         id = request.cookies.get('id', '').strip()
#         token = request.cookies.get('token', '').strip()
#         response.cookies.add_cookie('id', id, max_age=Config['time']['three_day'])
#         response.cookies.add_cookie('token', token, max_age=Config['time']['three_day'])


if __name__ == "__main__":
    app.run(
        host=Config['server']['host'],
        port=Config['server']['port'],
        # debug=True,
        access_log=True,
        auto_reload=True,
    )
