from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "wust-school"

    url = "http://jwc.wust.edu.cn/1881/list.htm"

    def parse(self, response):
        for url in data_from_xpath(response, '//ul[@class="news_list list2"]/li/span/a/@href', urls=True):
            yield self.process_item(url=url)

    @classmethod
    def process_detail(cls, response, document, info):
        table = response.xpath('//table[@class="wp_editor_art_table"]')
        all_tr = TableParser.from_html(table).strip().zip()
        for tr in all_tr:
            info.update(tr)
            print(info)
            yield info





if __name__ == "__main__":
    # MySpider.cza_run_spider()
    # MySpider.file_download()
    MySpider.file_reParse()