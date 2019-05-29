from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    page = 1
    url = 'http://www.sxcredit.gov.cn/queryPermitPublishPage.jspx'
    data = {
        "lb": "xzcf",
        "pageNo": str(page),
        "pageSize": "10",
    }

    def start_requests(self):
        yield FormRequest(self.url, formdata=self.data)

    def parse(self, response):
        print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
