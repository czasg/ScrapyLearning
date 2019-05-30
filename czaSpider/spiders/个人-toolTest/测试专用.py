from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class testMiddleWare():
    def process_response(self, request, response, spider):
        print(response.text)
        return response
    def process_request(self, request, spider):
        request.meta["hello"] = "world"
        pass

class MySpider(IOCO):
    name = "world-test"

    page = 1
    url = 'http://www.sxcredit.gov.cn/queryPermitPublishPage.jspx'
    data = {
        "lb": "xzcf",
        "pageNo": str(page),
        "pageSize": "10",
    }
    custom_settings = {"DOWNLOADER_MIDDLEWARES":
                           {"czaSpider.spiders.个人-toolTest.测试专用.testMiddleWare":100}}

    def start_requests(self):
        yield FormRequest(self.url, formdata=self.data)

    def parse(self, response):
        print(response.meta["hello"])
        # print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
