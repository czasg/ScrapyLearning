import time
import logging

logging = logging.getLogger(__name__)


class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        di = dict(item)
        di.setdefault("download_time", time.time())
        try:
            logging.info('document insert done!, counts: %d' % spider.mongo.source.insert(di).docs)
        except:
            logging.warning('Can Not Insert Documents Into Mongodb!')
        return item
