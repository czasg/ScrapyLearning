from czaSpider.czaBaseSpider import IOCO

from minitools.scrapy.extensions import close_spider_without_incfement


class MySpider(IOCO):
    name = "test_closespiderwithoutincrement"

    url = "http://fanyi.youdao.com/"
    custom_settings = close_spider_without_incfement

    def parse(self, response):
        import time
        time.sleep(10)
        yield response.request.replace(dont_filter=True)


if __name__ == '__main__':
    MySpider.cza_run_spider()
