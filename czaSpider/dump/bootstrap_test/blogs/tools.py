import hashlib

from models import *
from error_man import *
from config import configs

COOKIE_NAME = 'czaOrz'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None:
        raise APIResourceError('tools', 'Not Admin')

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except:
        pass
    return 1 if p < 1 else p

def user2cookie(user, max_age):
    expires = str(time.time() + max_age)
    s = "%s-%s-%s-%s" % (user.id, user.passwd, expires, _COOKIE_KEY)
    cookie = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
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


