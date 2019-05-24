from czaSpider.czaBaseSpider import IOCO


class MySpider(IOCO):
    name = "world-test"

if __name__ == "__main__":
    MySpider.mongodb2csv(resolver=True)
    # MySpider.cza_run_spider()
