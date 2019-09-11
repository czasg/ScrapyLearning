import re
import hashlib

from datetime import datetime

from database.mysql.models import *
from tools.error_man import *
from config import configs

COOKIE_NAME = 'czaOrz'
_COOKIE_KEY = configs.session.secret
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

ANTI_COOKIE_FIRST = 'anti_spider_first'
ANTI_COOKIE_SECOND = 'anti_spider_second'

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIResourceError('非管理员用户，无发执行此类操作', 'Not Admin')


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


def get_page_index(page_str):
    p = 1
    page_str = page_str[0] if isinstance(page_str, list) else page_str
    try:
        p = int(page_str)
    except:
        pass
    return 1 if p < 1 else p


def get_page_size(page_str):
    p = 6
    page_str = page_str[0] if isinstance(page_str, list) else page_str
    try:
        p = int(page_str)
    except:
        pass
    return 6 if p < 6 else p


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


def check_anti_spider(anti_cookie):
    return anti_cookie


def process_commands(all=None, size=None, ne=None, gt=None, gte=None, lt=None, lte=None, **kwargs):
    commands = []
    if kwargs:
        commands.append(kwargs)
    if all:  # {key:[v1,v2]}
        commands.append({key: {"$all": value} for key, value in all.items()})
    if size:  # {key:value}
        commands.append({key: {"$size": value} for key, value in size.items()})
    if ne:
        commands.append({key: {"$ne": value} for key, value in ne.items()})
    if gt:
        commands.append({key: {"$gt": value} for key, value in gt.items()})
    if gte:
        commands.append({key: {"$gte": value} for key, value in gte.items()})
    if lt:
        commands.append({key: {"$lt": value} for key, value in lt.items()})
    if lte:
        commands.append({key: {"$lte": value} for key, value in lte.items()})
    query = {"$and": commands} if commands else {}
    return query

def get_now_datetime():
    __date = datetime.now()
    return datetime(__date.year, __date.month, __date.day)


class Pager:
    def __init__(self, item_count, page_index=1, page_size=6):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index > self.page_count):
            self.page_index = 1
            self.offset = 0
            self.limit = 0
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % \
               (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__


import weakref
import collections
from functools import wraps
class LocalCache:
    notFound = object()

    class Dict(dict):
        def __del__(self):
            pass

    def __init__(self, maxLen=10):
        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=maxLen)

    @staticmethod
    def getNowTime():
        return int(time.time())

    def get(self, key):
        value = self.weak.get(key, self.notFound)
        if value is self.notFound or self.getNowTime() > value[r'expire']:
            return self.notFound
        return value

    def set(self, key, value):
        self.weak[key] = strongRef = LocalCache.Dict(value)
        self.strong.append(strongRef)


def miniCache(expire=60 * 60 * 12):
    caches = LocalCache()
    def wrapper(func):
        @wraps(func)
        async def wrapper1(*args, **kwargs):
            key = func.__name__
            result = caches.get(key)
            if result is caches.notFound:
                result = await func(*args, **kwargs)
                caches.set(key, {r'result': result, r'expire': expire + caches.getNowTime()})
                return result
            else:
                result = result[r'result']
                return result
        return wrapper1
    return wrapper
