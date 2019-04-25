from czaSpider.czaBaseSpider import czaSpider
from czaSpider.czaTools import *
"""
test the basic function of the framework
"""

class MySpider(czaSpider):
    name = "test-housePrice"
    author = "czaOrz"
    collName = get_collection_name(name, timeStr=True)  # TODO, if ot exist return cls(MySpider) way to init?
    dbName = get_database_name(name)  # TODO, if it can do self.__class__() ot init the property

    url = "http://sz.ziroom.com/z/nl/z3-d23008679-b612400051.html?p=1"

    def parse(self, response):
        print(response.url)


if __name__ == "__main__":
    MySpider.cza_run_spider()
