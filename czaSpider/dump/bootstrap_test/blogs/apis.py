import json
import logging

from aiohttp import web

from handler import get, post
from tools import *


logger = logging.getLogger(__name__)

@get('/')
async def index():
    return {'__template__': 'index.html'}


@get('/test')
async def login():
    print('login')
    return {'__template__': 'index.html'}

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    res = web.HTTPFound(referer or '/')
    res.set_cookie(COOKIE_NAME, '-deleted-', max_age=0)
    logger.info('user signed out!')
    return res

@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email or not passwd:
        raise APIResourceError('apis-authenticate', '请输入有效的: 用户名/密码')
    user = await User.findAll('email=?', [email])
    if len(user) == 0:
        raise APIResourceError('apis-authenticate', '用户名不存在')
    user = user[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode())
    sha1.update(b':')
    sha1.update(passwd.encode())
    if user.passwd != sha1.hexdigest():
        raise APIResourceError('apis-authenticate', '密码错误')
    res = web.Response()
    res.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    res.content_type = 'application/json'
    res.body = json.dumps(user, ensure_ascii=False).encode()
    return res
