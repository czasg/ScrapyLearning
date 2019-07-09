from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    url = "http://xxgk.beihai.gov.cn/bhshjbhj/xzzfzl_84504/index.html"

    def parse(self, response):
        yield from traverse_urls(response, self, '//ul[@class="bhdh_List"]/li/a/@href', 'index_%d', jump=1,
                                 next_page_without_new_urls=True)


if __name__ == "__main__":
    MySpider.cza_run_spider()
