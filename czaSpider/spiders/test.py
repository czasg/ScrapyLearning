from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *
"""
test the basic function of the framework
"""

class MySpider(IOCO):
    name = "test"

    urls = ["http://sz.ziroom.com/z/nl/z3-d23008679-b612400051.html?p=1", "http://jxj.beijing.gov.cn/xyData/front/creditService/initial.shtml?typeId=4"]

    def parse(self, response):
        print(response.url)


if __name__ == "__main__":
    MySpider.cza_run_spider()
