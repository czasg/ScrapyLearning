import time, hashlib

from project_config.config import configs
from tools.man_error import *
from database.mysql.models import User

COOKIE_NAME = 'czaOrz'
_COOKIE_KEY = configs.session.secret


def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIResourceError('非管理员用户，无发执行此类操作', 'Not Admin')


def user2cookie(user, max_age):
    expires = str(time.time() + max_age)
    s = "%d-%s-%s-%s" % (user.id, user.passwd, expires, _COOKIE_KEY)
    cookie = [str(user.id), expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(cookie)


async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if float(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = "%s-%s-%s-%s" % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            return None
        user.passwd = '******'
        return user
    except:
        return None
