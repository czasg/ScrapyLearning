import logging

logging = logging.getLogger(__name__)


class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        di = dict(item)
        more = di.get("more", {})
        di.setdefault("unique_flag", more.pop("unique_flag", "URL"))
        try:
            logging.info('document insert done!, counts: %d' % \
                         spider.mongo.resolver.insert(di).docs)
        except:
            logging.warning('Can Not Insert Documents Into MongoDB!')
        return item
