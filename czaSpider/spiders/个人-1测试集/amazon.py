from czaSpider.czaBaseSpider import czaSpider
from czaSpider.czaTools import *


class MySpider(czaSpider):
    name = "test123"
    custom_settings = {"ITEM_PIPELINES":
                           {"czaSpider.pipelines.temp.tempPipeline":300}}
    SQLITE3 = True

    url = "https://www.amazon.cn/s?k=men+wallet&" \
          "__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&" \
          "crid=28WXL2JBCQRQC&sprefix=men+wa%2Caps%2C133&ref=nb_sb_ss_i_1_6"

    def parse(self, response):
        res = data_from_xpath(response, '//span[@class="a-price"]/span[@class="a-offscreen"]/text()', returnList=True)
        print(len(res))
        print(res)
if __name__ == "__main__":
    MySpider.cza_run_spider()