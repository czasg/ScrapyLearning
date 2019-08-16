from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *
from czaSpider.middlewares import AntiJsClearanceMiddleware_setting, userAgentMiddleware_setting

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
headers = {'User-Agent': UA}
class MySpider(IOCO):
    name = "工商爬虫测试1"
    url = "http://www.gsxt.gov.cn/corp-query-entprise-info-searchBranch.html?entName="
    custom_settings = {'HTTPERROR_ALLOWED_CODES': {521, 403}}
    #                    **AntiJsClearanceMiddleware_setting,
    #                    **userAgentMiddleware_setting}

    def start_requests(self):
        url = "http://www.gsxt.gov.cn/corp-query-entprise-info-searchBranch.html?entName=福建福盈汽车销售服务有限公司"
        # yield Request(self.url+'福建福盈汽车销售服务有限公司', headers=headers)
        yield Request(url)

    def parse(self, response):
        print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
