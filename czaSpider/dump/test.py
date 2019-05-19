from czaSpider.czaBaseSpider import czaSpider
from czaSpider.czaTools import *

# http://sthjj.taian.gov.cn/art/2016/10/13/art_46686_5015303.html
# http://sthjj.taian.gov.cn/art/2016/6/30/art_46686_5015307.html

class MySpider(czaSpider):


    def parse(self, response):
        print(response.text)

def func(doc=None, **kwargs):
    print(doc or kwargs)


if __name__ == "__main__":
    func(**{"URL":"123"})
    func({"URL":"123"})
    # MySpider.cza_run_spider()
    from importlib import import_module
    # from czaSpider.dataBase.mysql_database import get_module_path
    # import logging
    # dbName = 'housePrice'
    # lib_path = get_module_path() + ".%sDB" % dbName
    # print(lib_path)
    # try:
    # import_module(lib_path)
    # except ImportError:
    #     logging.warning('import lib failure')
    # from czaSpider.dataBase.mysql_database import models
    # print(hasattr(models, 'housePriceDB'))
    # func(test="123")
    # from czaSpider.dataBase.config import REDIS_INFO
    # print(REDIS_INFO)


