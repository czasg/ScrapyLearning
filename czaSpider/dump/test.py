from czaSpider.czaBaseSpider import IOCO


class MySpider(IOCO):
    name = "world123"

    url = "http://www.baidu.com/"

    def parse(self, response):
        print(self.crawler.settings.get("testCommand", None))

    @classmethod
    def cza_run_spider(cls):
        import os
        os.system("scrapy crawl {} -s testCommand={}".format(cls.name, "cza"))

if __name__ == "__main__":
    # MySpider.mongodb2csv(resolver=True)
    MySpider.cza_run_spider()
