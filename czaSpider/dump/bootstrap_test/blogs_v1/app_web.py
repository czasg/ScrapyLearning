#!/usr/bin/env python3
import logging

from database.mysql import orm

from jinja2 import Environment, FileSystemLoader

from tools.public_func import *
from tools.safe_check_spider import *
from tools.safe_check_user import *
from tools.handler import *
from database.redis.database_redis import *
from database.mysql.models import *

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)


def init_jinja2(app, **kwargs):
    options = dict(
        autoescape=kwargs.get('autoescape', True),
        block_start_string=kwargs.get('block_start_string', '{%'),
        block_end_string=kwargs.get('block_end_string', '%}'),
        variable_start_string=kwargs.get('variable_start_string', '{{'),
        variable_end_string=kwargs.get('variable_end_string', '}}'),
        auto_reload=kwargs.get('auto_reload', True)
    )
    path = kwargs.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kwargs.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env


async def init_user2redis():
    users = await User.findAll()
    if users:
        for user in users:
            redis_handler.hset(REDIS_USER_SNOW_ID, user.id, user.name)


async def anti_spider_first(app, handler):  # todo 反爬需要单独起一个服务，不然别的服务就没法使用了
    async def _anti_spider_first(request):
        anti_cookie = request.cookies.get(ANTI_COOKIE_FIRST)
        if not request.path.startswith(('/get/anti/spider/first', '/api/', '/static/')):
            if anti_cookie:
                anti = check_anti_spider(anti_cookie)
                if anti == 'True':
                    pass
                else:
                    return web.HTTPForbidden()
            else:
                res = web.Response(body=app['__templating__'].get_template('anti_spider/anti_spider_first.html').
                                   render(**{'anti_spider_path': request.path}).encode('utf-8'))
                res.content_type = 'text/html;charset=utf-8'
                return res
        return (await handler(request))

    return _anti_spider_first


async def anti_spider_second(app, handler):
    async def _anti_spider_second(request):
        anti_cookie = request.cookies.get(ANTI_COOKIE_SECOND)
        if request.path.startswith(('/get/anti/spider/second', '/api/', '/static/', '/favicon.ico')):
            return (await handler(request))
        if anti_cookie != stringToHex(request.path):
            res = web.Response(body=app['__templating__'].get_template('anti_spider/anti_spider_second.html').
                               render(**{'anti_spider_path': request.path}).encode('utf-8'))
            # res.set_cookie(ANTI_COOKIE_SECOND, '-deleted-', max_age=0)
            res.set_cookie(ANTI_COOKIE_SECOND, stringToHex(request.path))
            res.content_type = 'text/html;charset=utf-8'
            return res
        return (await handler(request))

    return _anti_spider_second


async def anti_spider_third(app, handler):
    async def _anti_spider_third(request):
        if request.path.startswith('/api/captcha/anti/spider/third'):
            if request.method != 'POST':
                return web.HTTPForbidden()
            params = await request.json()
            if 'captcha_value' not in params:
                return process_json(dict(error='请求参数错误'))
            right_answer = redis_handler.get(request.remote + ':captcha')
            if not right_answer:
                return process_json(dict(error='验证码已失效'))
            if right_answer.decode() == params.get('captcha_value'):
                redis_handler.set(request.remote, 1, COUNT_EXPIRE_TIME)
                return process_json(dict(success='验证成功'))
            else:
                return process_json(dict(error='验证码错误，请检查大小写是否正确'))
        if request.path.startswith(('/static/', '/api/', '/favicon.ico')):  # todo 这个'/favicon.ico'好讨厌啊
            return (await handler(request))
        times_record = redis_handler.hget(REDIS_ANTI_SPIDER_TIME, request.remote)
        count_record = int(redis_handler.get(request.remote) or 0)

        if not times_record:
            redis_handler.hset(REDIS_ANTI_SPIDER_TIME, request.remote, get_now_time_stamp())
        elif (get_now_time_stamp() - int(times_record)) < 3:
            logger.warning(request.path)
            logger.warning('%s 访问过频繁，记录1次，当前次数 %d' % (request.remote, count_record))
            redis_handler.incr(request.remote)
        redis_handler.hset(REDIS_ANTI_SPIDER_TIME, request.remote, get_now_time_stamp())

        if not count_record:
            redis_handler.set(request.remote, 1, COUNT_EXPIRE_TIME)
        elif count_record < COUNT_CAPTCHA_TIME:
            pass
        elif count_record < COUNT_FORBID_TIME:
            logger.error(request.path + str(count_record))
            result, captcha_picture = next_captcha()
            redis_handler.set(request.remote + ':captcha', result, CAPTCHA_EXPIRE_TIME)
            if request.path.startswith('/api/captcha/change'):
                return process_json({'captcha_picture': captcha_picture})
            res = web.Response(body=app['__templating__'].get_template('anti_spider/anti_spider_third.html').
                               render(**{'captcha_picture': captcha_picture}).encode('utf-8'))
            res.content_type = 'text/html;charset=utf-8'
            return res
        else:
            return web.HTTPForbidden()
        return (await handler(request))

    return _anti_spider_third


async def auth_factory(app, handler):
    async def auth(request):
        logger.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            logger.info('Request with COOKIE')
            user = await cookie2user(cookie_str)
            if user:
                logger.info('Valid user, set current user: %s' % user.email)
                request.__user__ = user
        else:
            logger.info('Request without COOKIE')
        return (await handler(request))

    return auth


async def response_factory(app, handler):
    async def response(request):
        logger.info('Response Handler .....')
        r = await handler(request)
        logger.info(r)
        if isinstance(r, web.StreamResponse):
            logger.info('StreamResponse! return directly')
            return r
        if isinstance(r, bytes):
            logger.info('Bytes! return directly!')
            return web.Response(body=r, content_type='application/octet-stream')
        if isinstance(r, str):
            logger.info('Str!')
            if r.startswith('redirect:'):
                logger.info('startswith redirect, reset to: %s' % str(r[9:]))
                return web.HTTPFound(r[9:])
            logger.info('return TEXT/HTML')
            res = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__)
                               .encode('utf-8'))
            res.content_type = 'text/html;charset=utf-8'
            return res
        if isinstance(r, dict):
            logger.info('Dict!')
            template = r.get('__template__', None)
            if template is None:
                logger.info('dict with out template!, return JSON')
                res = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__)
                                   .encode('utf-8'))
                res.content_type = 'application/json;charset=utf-8'
                return res
            else:
                logger.info('return template: %s' % str(template))
                r['__user__'] = request.__user__
                res = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                res.content_type = 'text/html;charset=utf-8'
                return res
        res = web.Response(body=str(r).encode('utf-8'))
        res.content_type = 'text/plain;charset=utf-8'
        return res

    return response


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


async def init(loop):
    await orm.init_pool(loop=loop, **configs.db)
    await init_user2redis()
    app = web.Application(loop=loop, middlewares=[
        anti_spider_first,
        # anti_spider_second, anti_spider_third,
        auth_factory, response_factory])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'apis')
    add_static(app)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 9000)
    logger.info('server started at http://127.0.0.1:9000...')
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
