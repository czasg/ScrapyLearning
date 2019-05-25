import logging

from redis import StrictRedis

from czaSpider.dataBase.config import REDIS_INFO

logging = logging.getLogger(__name__)


def get_redis_client():
    try:
        client = StrictRedis(**REDIS_INFO)
    except:
        logging.warning('redis connect failed!')
        raise Exception('redis connect error')
    else:
        logging.info('connect redis')
        return client


class BaseRedis:
    def __init__(self, dbName, collName):
        self.client = get_redis_client()
        self._memoryName = dbName + collName
        self._memoryCount = dbName + collName + "-count:"
        self._menNums = 0  # _memoryName
        self._memCounts = 0  # _memoryCount
        self._docs = None
        self._init_memory_count()

    @property
    def name(self):
        return self._memoryName

    @property
    def memCount(self):
        return int(self._memCounts)

    @property
    def memNum(self):
        return int(self._menNums)

    @property
    def doc(self):
        docs = self._docs
        self._docs = None
        return docs

    def _init_memory_count(self):
        self.client.set(self._memoryCount, 0)
        if self.client.exists(self._memoryName):
            self._menNums = self.client.scard(self._memoryName)

    def inc_memCount(self):
        self.client.incr(self._memoryCount)
        self.refresh()
        return self

    def refresh(self):
        self._menNums = self.client.scard(self._memoryName)
        self._memCounts = self.client.get(self._memoryCount)
        return self

    def push(self, *args):
        self.client.sadd(self._memoryName, *args)
        self.refresh()
        return self

    def pop(self):
        self._docs = self.client.spop(self._memoryName)
        return self

    def exist(self):
        return self.client.exists(self._memoryName)

    def close(self):
        self.client.delete(self._memoryName)
        self.client.delete(self._memoryCount)
