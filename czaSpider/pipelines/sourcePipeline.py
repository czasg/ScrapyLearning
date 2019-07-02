import logging

logger = logging.getLogger(__name__)


class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        di = dict(item)
        more = di.get("more", {})
        di.setdefault("unique_flag", more.pop("unique_flag", "URL"))
        di.setdefault("download_finished", False)
        try:
            logger.info('document insert done!, counts: %d' % spider.mongo.source.insert(di).docs)
        except:
            logger.warning('Can Not Insert Documents Into Mongodb!')
        return item
