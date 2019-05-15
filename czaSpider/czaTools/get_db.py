import os
import time
import pymongo
import sqlite3
import redis

from czaSpider.settings import MONGO_INFO,sqlite3_INFO,REDIS_INFO,shubo_mongo
from czaSpider.czaTools.path_func import get_current_path, to_path, get_database_path


def get_mongo_client():
    return pymongo.MongoClient(**MONGO_INFO)


def get_redis_client():
    pass

