import weakref
import collections
import time

from functools import wraps


def miniCache(expire=60 * 60 * 12):
    caches = LocalCache()

    def wrapper(func):
        @wraps(func)
        def wrapper1(request):
            key = func.__name__

            day = str(request.GET.get('day', ''))
            filter_province = '0000' if request.GET.get('just_choose_province', None) == 'true' else ''
            key += (day + filter_province)

            result = caches.get(key)
            if result is caches.notFound:
                result = func(request)
                caches.set(key, {r'result': result, r'expire': expire + caches.getNowTime()})
                return result
            else:
                result = result[r'result']
                return result

        return wrapper1

    return wrapper


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
