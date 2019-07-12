import time
import logging

logger = logging.getLogger(__name__)


class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        di = dict(item)
        di.setdefault("download_time", time.time())
        try:
            logger.info('document insert done!, counts: %d' % spider.mongo.source.insert(di).docs)
        except:
            logger.warning('Can Not Insert Documents Into Mongodb!')
        return item
