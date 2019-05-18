from czaSpider.czaTools import *
from .czaBaseItem import czaBaseItem, process_base_item


class Item(czaBaseItem):
    # 此处继承父类，并指定需要拓展的类
    goods_price = scrapy.Field()
    goods_name = scrapy.Field()

def goodsItem(**kwargs):
    item = Item()
    item["goods_price"] = kwargs.pop('goods_price', None)
    item["goods_name"] = kwargs.pop('goods_name', None)
    item.update(process_base_item(**kwargs))
    return item