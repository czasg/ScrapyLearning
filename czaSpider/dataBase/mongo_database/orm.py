import logging
import pymongo

from czaSpider.dataBase.config import MONGO_INFO


def get_mongo_client():
    return pymongo.MongoClient(**MONGO_INFO)

# todo, add orm about update, insert, remove, find
