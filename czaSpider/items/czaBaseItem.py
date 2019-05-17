from czaSpider.czaTools import *


class czaBaseItem(scrapy.Item):
    spiderName = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    more = scrapy.Field()


def process_base_item(**kwargs):
    info = {}
    info["spiderName"] = kwargs.pop('spiderName', "IOCO")
    info["author"] = kwargs.pop('author', "czaOrz")
    info["url"] = kwargs.pop('url', None)
    info["more"] = kwargs
    return info
