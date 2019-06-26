#!/usr/bin/env python3
import json


from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import orm

from tools import *
from handler import *
from config import configs

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


def init_jinja2(app, **kwargs):
    logger.info('init jinja2...')
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
    logger.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kwargs.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

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
        # if request.path.startswith('/manage/') and request.__user__ is None:
        #     logger.info('Invalid __user__: %s, Redirect to sign_in!' % request.__user__)
        #     return web.HTTPFound('/signin')  # todo, here is the 302
        return (await handler(request))

    return auth

async def response_factory(app, handler):
    async def response(request):
        logger.info('Response Handler .....')
        r = await handler(request)
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
    app = web.Application(loop=loop, middlewares=[
        auth_factory, response_factory])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'apis')
    # add_routes(app, 'api')  # todo, 待转移到这边来，分类进行管理
    add_static(app)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 9000)
    logger.info('server started at http://127.0.0.1:9000...')
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
