from czaSpider.czaTools import *
from .czaBaseItem import czaBaseItem, process_base_item


class Item(czaBaseItem):
    # 此处继承父类，并指定需要拓展的类
    source = scrapy.Field()


def sourceItem(**kwargs):
    item = Item()
    item.update(process_base_item(**kwargs))

    item["source"] = kwargs.pop('source', None)
    return item
