import logging

logging = logging.getLogger(__name__)

import time

from threading import Thread
from bson import ObjectId

from czaSpider.dataBase.redis_database.orm import BaseRedis
from czaSpider.czaTools import *
from .fileManager import FileManager
from .baseDownloader import BaseDownloader


# class Record(dict):
#     def __init__(self, **kwargs):
#         super(Record, self).__init__(**kwargs)
#
#     def __getattr__(self, key):
#         return self[key]
#
#     def __setattr__(self, key, value):
#         self[key] = value


class Downloader(BaseDownloader):
    def __init__(self, spider, **kwargs):
        super(Downloader, self).__init__(**kwargs)
        self.spider = spider
        self.buffer = 0
        self.record = None

        self.thread = kwargs.get('thread', 1)
        self.delay = kwargs.get('delay', 0)
        self.tolerate = kwargs.get('tolerate', 0)
        self.allow_download_fail = kwargs.get('allow_download_fail', False)

        self.redis = BaseRedis(spider.dbName, spider.collName)
        self._init_redis_from_mongodb()

    def _init_redis_from_mongodb(self):
        if self.redis and self.spider.mongo:
            if self.redis.exist():
                logging.warning('redis: %s had existed, using it' % self.redis.name)
            else:
                docs = self.spider.mongo.source.findAll(download_finished=False, field={'_id': 1}).documents
                if not docs:
                    logging.warning('%s have download finished!' % self.spider.name)
                else:
                    self.buffer = self.redis.push(*docs).memNum

    def start(self):
        threads = [Thread(target=self.worker, name='joker-%d' % t) for t in range(self.thread)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.redis.close()

    def worker(self):
        while True:
            if not self._next():  # new record -> Record
                break
            self._downloader()  # download and update record to mongodb

    def _next(self):
        _id = self.redis.pop().doc
        if not _id:
            return 0
        self.record = Record(**self.spider.mongo.source.find(_id=ObjectId(_id)).documents)
        if not self.record or self.record.download_finished:
            return self._next()
        return 1

    def _downloader(self):
        requests = self.record.source  # list
        fm = [FileManager(**r).process(download=self.download) for r in requests]
        files = [f.requests for f in fm]
        for f in fm:
            if f.fid or self.allow_download_fail:
                self.record.download_finished = True
        self.record.source = files
        self.spider.mongo.source.update(_id=self.record._id, set=self.record)
        logging.warning('download: %s' % self.redis.inc_memCount().memCount)
        time.sleep(self.delay)
