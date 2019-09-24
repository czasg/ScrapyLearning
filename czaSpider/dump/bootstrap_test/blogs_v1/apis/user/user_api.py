import json

from tools.handler import get, post, web
from tools.man_pager import get_page_index, Pager
from tools.public_func import _RE_SHA1, _RE_EMAIL
from tools.safe_check_user import *
from database.mysql.models import *
from database.redis.database_redis import *


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email or not passwd:
        raise APIResourceError('请输入有效的: 用户名/密码', 'apis-authenticate')
    user = await User.findAll('email=?', [email])
    if len(user) == 0:
        raise APIResourceError('用户名不存在', 'apis-authenticate')
    user = user[0]
    sha1 = hashlib.sha1()
    sha1.update(str(user.id).encode())
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
    if email == 'root@ioco.com':
        raise APIResourceError('无法注册root用户', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%d:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='/static/img/user.png')
    await user.save()
    redis_handler.hset(REDIS_USER_SNOW_ID, user.id, user.name)
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
    sha1_passwd = '%d:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, admin=True,
                passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='/static/img/user.png')
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@post('/api/drop/user')
async def api_drop_user(request, *, id):
    check_admin(request)
    if request.__user__.id == id:
        raise APIResourceError('root用户无法删除，请联系管理员', 'root User can not be drop')
    user = await User.find(id)
    blogs = await Blog.findAll('user_id=?', [id])
    for blog in blogs:
        comments = await Comment.findAll('blog_id=?', blog.id)
        for comment in comments:
            await comment.remove()
        await blog.remove()
    await user.remove()
    redis_handler.hdel(REDIS_USER_SNOW_ID, id)
    return {'id': id}


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
        u['id'] = str(u['id'])
    return dict(page=p, users=users)
