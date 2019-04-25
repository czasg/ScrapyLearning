from czaSpider.czaTools import *


class czaBaseItem(scrapy.Item):
    spiderName = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    releaseTime = scrapy.Field()
    more = scrapy.Field()


def process_base_item(**kwargs):
    info = {}
    info["spiderName"] = kwargs.pop('spiderName', "czaSpider")
    info["author"] = kwargs.pop('author', "czaOrz")
    info["url"] = kwargs.pop('url', None)
    info["releaseTime"] = kwargs.pop('releaseTime', get_now_time())
    info["more"] = kwargs.pop('more', None)
    return info
