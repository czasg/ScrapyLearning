from czaSpider.dataBase.file_database.fileManager import FileManager
from czaSpider.czaTools import *
from .czaBaseItem import czaBaseItem, process_base_item


class Item(czaBaseItem):
    # 此处继承父类，并指定需要拓展的类
    source = scrapy.Field()


def sourceItem(spider, **kwargs):
    item = Item()
    html = kwargs.pop('html', None)
    item.update(process_base_item(**kwargs))

    source = html or item['url']
    source = source if isinstance(source, list) else [source]
    item['source'] = [FileManager(request=request).process(close=True).requests for request in source]
    return item
