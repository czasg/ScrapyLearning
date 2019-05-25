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
            record = self._next()
            if not record:  # new record -> Record
                break
            self._downloader(record)  # download and update record to mongodb

    def _next(self):
        _id = self.redis.pop().doc
        return Record(**self.spider.mongo.source.find(_id=ObjectId(_id)).documents) if _id else None

    def _downloader(self, record):
        record.download_finished = True
        fm = [FileManager(**rs).process(download=self.download) for rs in record.source]
        for f in fm:
            if not f.fid and not self.allow_download_fail:
                record.download_finished = False
        record.source = [f.requests for f in fm]
        self._dynamic_download_rate_log(self.spider.mongo.source.update(_id=record._id, set=record))
        time.sleep(self.delay)

    def _dynamic_download_rate_log(self, _):
        count = self.redis.inc_memCount().memCount
        percentage = count * 100 // self.buffer
        print('\r' + 'download rate: %d/%d %d%% ' % (count, self.buffer, percentage) + '#' * (percentage // 2), end='',
              flush=True)
