from czaSpider.czaBaseSpider import czaSpider
from czaSpider.czaTools import *


class MySpider(czaSpider):
    name = "zlzp-jobPosition"
    author = "czaOrz"
    collName = get_collection_name(name, timeStr=True)
    dbName = get_database_name(name)
    # custom_settings = get_custom_settings(name)