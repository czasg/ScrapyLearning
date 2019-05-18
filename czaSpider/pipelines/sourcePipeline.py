import logging
logging = logging.getLogger(__name__)

class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        di = dict(item)
        more = di.get("more", {})
        di.setdefault("unique_flag", more.pop("unique_flag", "URL"))
        di.setdefault("download_finished", False)  # todo, first, all is False, even it has push to file-sever
        try:  # todo, just wait for file-manager to polish twice
            logging.info('document insert done!, counts: %d' % spider.mongo.source.insert(di).docs)
        except:
            logging.warning('Can Not Insert Documents Into Mongodb!')
        return item
