from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "hello-test2"

    url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+++2019-07-24%20TO%202019-07-25+%E4%B8%8A%E4%BC%A0%E6%97%A5%E6%9C%9F:2019-07-24%20TO%202019-07-25&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6"

    def parse(self, response):
        print(response.text)

if __name__ == '__main__':
    MySpider.cza_run_spider()