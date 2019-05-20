import logging

from threading import Thread
from bson import ObjectId

from czaSpider.dataBase.redis_database.orm import BaseRedis
from czaSpider.czaTools import *
from .fileManager import FileManager
from .baseDownloader import BaseDownloader

logging = logging.getLogger(__name__)


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
                self.buffer = self.redis.memNum
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
        for f in fm:
            if f.fid or self.allow_download_fail:
                self.record.download_finished = True
        self.record.source = [f.requests for f in fm]
        self._dynamic_download_rate_log(self.spider.mongo.source.update(_id=self.record._id, set=self.record))
        time.sleep(self.delay)

    def _dynamic_download_rate_log(self, _):
        count = self.redis.inc_memCount().memCount
        percentage = count * 100 // self.buffer
        print('\r' + 'download rate: %d/%d %d%% ' % (count, self.buffer, percentage) + '#' * (percentage // 2), end='',
              flush=True)
