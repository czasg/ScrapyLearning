from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

# 313932302c31303830
class MySpider(IOCO):
    name = "yuns-yuns"

    url = "http://www.xjboz.gov.cn/zwdt/bzdt.htm"

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    MySpider.cza_run_spider()
