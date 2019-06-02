from czaSpider.czaBaseSpider import IOCO
from czaSpider.middlewares import AntiJsClearanceMiddleware_setting


class MySpider(IOCO):
    name = "银监会-test"

    handle_httpstatus_list = [521]
    custom_settings = AntiJsClearanceMiddleware_setting

    url = "http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current=1"

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    MySpider.cza_run_spider()
