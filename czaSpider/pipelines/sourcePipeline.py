import logging

class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        item["source"] = []
        di = dict(item)
        more = di.get("more", {})
        di.setdefault("unique_flag", more.pop("unique_flag", "URL"))
        try:
            logging.info('document insert done!, counts: %d' % spider.mongo.insert(di).docs)
        except:
            logging.warning('Can Not Insert Documents Into MongoDB!')
        return item
