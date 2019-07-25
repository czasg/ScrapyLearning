from redis import StrictRedis
from random import choice

REDIS_KEY = 'czatest'
class RedisClient:
    def __init__(self):
        self.db = StrictRedis('127.0.0.1', port=6379)

    def add(self, proxy, score=10):
        if not self.db.zscore(REDIS_KEY, proxy):
            print('???')
            return self.db.zadd(REDIS_KEY, **{proxy: score})

    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, 0, 100)
        if result:
            return choice(result)
        else:
            raise Exception()

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > 0:
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        return self.db.zadd(REDIS_KEY, **{proxy: 100})

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, 0, 100)

    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop-1)

if __name__ == '__main__':
    conn = RedisClient()
    # result = conn.batch(1, 10)
    # print(result)

    # print(conn.count())
    # print(conn.all())
    # print(conn.max('test1'))
    # print(conn.decrease('test1'))
    # print(conn.exists('test1'))
    print(conn.random())
    # for i in range(10):
    #     conn.add('test%d' % i)



