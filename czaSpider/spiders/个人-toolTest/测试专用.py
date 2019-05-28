from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    # http://www.zzcredit.gov.cn/xzcf/
    url1 = "http://www.zzcredit.gov.cn/xzcf/"
    url2 = "http://www.zzcredit.gov.cn/selectSgsInfo.jspx"
    data = {
        "type":"frcf",
        "keyword":"",
        "belongsArea": "",
        "bm": "",
        "pageSize": "12",
        "pageNo": "1",
        "_":"1559037829564"
    }
    header = {
        "Referer":"http://www.zzcredit.gov.cn/xzcf/",
        "User-Agent":""
    }

    def start_requests(self):
        yield FormRequest(self.url2, formdata=self.data, method="GET")

    def parse(self, response):
        print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
