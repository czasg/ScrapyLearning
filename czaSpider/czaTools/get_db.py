import os
import time
import pymongo
import sqlite3
import redis

from czaSpider.settings import MONGO_INFO,sqlite3_INFO,REDIS_INFO
from czaSpider.czaTools.path_func import get_current_path, to_path, get_database_path


def get_mongo_client():  # todo, wait for abandon
    return pymongo.MongoClient(**MONGO_INFO)


def get_redis_client():
    pass

#
# r.lpush('dbName', 'hello')
# a = r.llen('dbName')
# print(a, type(a), 'he')

# r.set()
# r.get()
# r.delete('dbName')
#
# r.hmset()
# r.hgetall()
#
# r.llen()
# r.lpush()
# r.lpop()
#
# r.sadd()
if __name__ == "__main__":
    r = redis.StrictRedis(decode_responses=True)
    # print(r.llen('dbName'))
    # r.set('counter', 0)
    # r.incr('counter')
    # print(r.get('counter'))
    print(r.exists('dbName'))