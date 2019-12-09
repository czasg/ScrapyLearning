# -*- coding: utf-8 -*-
from minitools.scrapy import miniSpider
import execjs, re
from pprint import pprint
from scrapy import FormRequest
with open('zgcpwsw2.js', encoding='utf-8') as f:
    js = f.read()
    anti_second = execjs.compile(js)
with open('zgcpwsw3.js', encoding='utf-8') as f:
    js = f.read()
    anti_third = execjs.compile(js)
def refresh_formData(page, vl5x, number, guid):
    formData = {
        "Param": '案件类型:刑事案件',  # 卧槽，还真和这个有强关联
        "Index": str(page),
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": str(vl5x),
        "number": 'oldw',
        "guid": str(guid),
    }
    return formData
class MySpider(miniSpider):
    start_urls = ["http://oldwenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=4f2514c2-9092-4c12-a4bf-a90600bd8006"]
    list_url = "http://oldwenshu.court.gov.cn/List/ListContent"
    # def start_requests(self):
    #     print("huibuhui zouzheli ne ")
    #     yield FormRequest(self.start_urls[0], method='GET', dont_filter=True)
    def parse(self, response):
        print(response.text)
        # import time
        # time.sleep(2)
        # yield response.request
    # def parse1(self, response):
    #     print(response.text)
if __name__ == '__main__':
    MySpider.run(__file__)
