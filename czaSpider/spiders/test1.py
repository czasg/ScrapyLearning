from czaSpider.czaBaseSpider import czaSpider
from czaSpider.czaTools import *

"""
test the table from html
it can translate the table to a dict
but just the first to key and other to value
"""


class MySpider(czaSpider):
    name = "test-web-table"
    # url = "http://sthjj.taian.gov.cn/art/2016/10/13/art_46686_5015303.html"
    url = "http://www.runoob.com/python/python-func-all.html"

    def parse(self, response):
        table = data_from_xpath(response, '//div[@class="m-newscontent"]//table')

        all_tr = TableParser.from_html(table).strip().zip()
        for di in all_tr:
            print(di)

        print('------Cutting Line------')
        all_tr = TableParser.from_html(table).strip().transpose().zip()
        for di in all_tr:
            print(di)
        print(xpather(response,'//div[@class="article-intro"]').article)

if __name__ == "__main__":
    MySpider.cza_run_spider()
