from czaSpider.czaTools import *
from .czaBaseItem import czaBaseItem, process_base_item


class Item(czaBaseItem):
    # 此处继承父类，并指定需要拓展的类
    house_price = scrapy.Field()
    house_place = scrapy.Field()
    house_name = scrapy.Field()
    house_area = scrapy.Field()
    house_floor = scrapy.Field()
    house_scale = scrapy.Field()
    distance_from_subway = scrapy.Field()

def housePriceItem(**kwargs):
    item = Item()
    item.update(process_base_item(**kwargs))

    item["house_price"] = kwargs.pop('house_price', None)
    item["house_place"] = kwargs.pop('house_place', None)
    item["house_name"] = kwargs.pop('house_name', None)
    item["house_area"] = kwargs.pop('house_area', None)
    item["house_floor"] = kwargs.pop('house_floor', None)
    item["house_scale"] = kwargs.pop('house_scale', None)
    item["distance_from_subway"] = kwargs.pop('distance_from_subway', None)
    return item
