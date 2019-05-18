import logging
logging = logging.getLogger(__name__)

from czaSpider.czaTools import *


class PropBaseSpider(scrapy.Spider):
    name = "IOCO"
    author = "czaOrz"

    dbName = None
    collName = None

    ALLOW_DOWNLOAD_FAIL = False
