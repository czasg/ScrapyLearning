from czaSpider.czaBaseSpider import IOCO


class MySpider(IOCO):
    name = "world-test"

    url = "http://www.baidu.com/"

    def parse(self, response):
        print(response.text)

if __name__ == "__main__":
    # MySpider.mongodb2csv(resolver=True)
    MySpider.cza_run_spider()
