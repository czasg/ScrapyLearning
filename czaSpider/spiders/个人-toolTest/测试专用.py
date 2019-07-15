from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    url = "http://huyu.info/"

    def parse(self, response):
        print(response.text)
        # yield from traverse_urls(response, self, '//ul[@class="bhdh_List"]/li/a/@href', 'index_%d', jump=1,
        #                          next_page_without_new_urls=True)


if __name__ == "__main__":
    MySpider.cza_run_spider()
