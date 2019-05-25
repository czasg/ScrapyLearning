from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

"""
"""


class MySpider(IOCO):
    name = "redis-test"

    url = "http://xxgk.wust.edu.cn/2593/list.htm"

    def parse(self, response):
        for i in range(30):
            yield self.process_item(url=response.url)


if __name__ == "__main__":
    # MySpider.cza_run_spider()
    MySpider.file_download(thread=3, delay=3)
    # MySpider.file_reParse()
    # MySpider.file_clear_downloaded()