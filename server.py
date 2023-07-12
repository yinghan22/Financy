import traceback

from sanic import Sanic
from sanic_ext import Extend
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

app.config.CORS_ORIGINS = '*'
app.config.CORS_ALLOW_HEADERS = '*'
app.config.CORS_EXPOSE_HEADERS = 'X-token'

Extend(app)


@app.route('/api/test')
async def test(request):
    return Response().success()


@app.exception(Exception)
async def handle_exception(request, exception):
    tb = traceback.extract_tb(exception.__traceback__)[-1]
    message = f"异常:{tb.filename}:{tb.lineno}:{tb.name}> {tb.line}. 异常信息: {str(exception)}."
    traceback.print_stack()
    traceback.print_exc()
    return Response().error(message=message)


@app.middleware('request')
async def auth_middleware(request):
    if request.method in ['OPTIONS', 'options']:
        res = Response().success()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = '*'
        res.headers['Access-Control-Expose-Headers'] = 'X-token'
        return res
    elif request.path != '/api/user/login':
        token = request.headers.get('X-token', '')
        if token == '':
            return Response().error(message='请重新登录')
        async with request.app.ctx.redis as redis:
            temp = await redis.get(f"token:{token}")
            if temp is None:
                return Response().error(message='请重新登录')
            else:
                await redis.set(f"token:{token}", token, ex=Config['time']['three_day'])


@app.middleware('response')
async def session_middleware(request, response):
    if request.method in ['options', 'OPTIONS']:
        pass
    elif request.path not in ['/api/user/login', '/api/user/logout']:
        token = request.headers.get('X-token', '')
        if token == '':
            response = Response().error(message='请重新登录')
            return
        async with request.app.ctx.redis as redis:
            temp = await redis.get(f"token:{token}")
            if temp is None:
                response = Response().error(message='请重新登录')
                return
            else:
                await redis.set(f"token:{token}", token, ex=Config['time']['three_day'])
                response.headers['X-token'] = token
                if response is None:
                    print('\nNone is Response')


if __name__ == "__main__":
    app.run(
        host=Config['server']['host'],
        port=Config['server']['port'],
        # debug=True,
        access_log=True,
        auto_reload=True,
    )
