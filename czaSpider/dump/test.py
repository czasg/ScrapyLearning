from czaSpider.czaBaseSpider import czaSpider
from czaSpider.czaTools import *

# http://sthjj.taian.gov.cn/art/2016/10/13/art_46686_5015303.html
# http://sthjj.taian.gov.cn/art/2016/6/30/art_46686_5015307.html

class MySpider(czaSpider):


    def parse(self, response):
        print(response.text)

if __name__ == "__main__":
    MySpider.cza_run_spider()


