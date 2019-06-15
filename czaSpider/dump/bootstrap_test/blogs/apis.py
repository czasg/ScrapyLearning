import json

from aiohttp import web

from handler import get, post
from tools import _RE_EMAIL, _RE_SHA1
from tools import *

logger = logging.getLogger(__name__)


# 模板页面 #

@get('/')
async def index(*, page='1'):  # todo，权宜之计，就是测试用的，首页不需要page参数，后序转到blog里面
    return {
        '__template__': 'index.html',
        'page_index': get_page_index(page)
    }


@get('/register')
async def register():
    return {'__template__': 'register.html'}


@get('/root/manage/users')
async def root_manage_users(request, *, page='1'):
    check_admin(request)
    return {
        '__template__': 'root_manage_users.html',
        'page_index': get_page_index(page)
    }


# 登陆认证、注册、退出模块 #

@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email or not passwd:
        raise APIResourceError('请输入有效的: 用户名/密码', 'apis-authenticate')
    user = await User.findAll('email=?', [email])
    if len(user) == 0:
        raise APIResourceError('用户名不存在', 'apis-authenticate')
    user = user[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode())
    sha1.update(b':')
    sha1.update(passwd.encode())
    if user.passwd != sha1.hexdigest():
        raise APIResourceError('密码错误', 'apis-authenticate')
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse

@post('/api/new/user')
async def api_register_user(*, name, email, passwd):
    if not name or not name.strip():
        raise APIResourceError('用户名不能为空', 'error Username')
    if not email or not _RE_EMAIL.match(email):
        raise APIResourceError('邮箱格式错误', 'error Email Format')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIResourceError('密码验证异常', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse

@post('/api/new/root/user')
async def api_register_root_user(*, name, email, passwd):
    root = await User.findAll('email=?', ['root@ioco.com'])
    if len(root) > 0:
        raise APIResourceError('root用户已存在，请勿创建', 'root user has already existed!')
    if not name or not name.strip():
        raise APIResourceError('用户名不能为空', 'error Username')
    if email != 'root@ioco.com':
        raise APIResourceError('无法识别root邮箱', 'error Email Format')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIResourceError('密码验证异常', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, admin=True,
                passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    webResponse = web.HTTPFound(referer or '/')
    webResponse.set_cookie(COOKIE_NAME, '-deleted-', max_age=0)
    logger.info('user signed out!')
    return webResponse


# json请求接口 #

@get('/api/get/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)


@get('/api/get/blogs')
async def api_get_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)

@post('/api/drop/user')
async def api_drop_user(request, *, name, email):
    check_admin(request)
    user = await User.findAll('email=?', [email])
    await user.remove()
    return {'warning': 'drop %s success!' % name}
