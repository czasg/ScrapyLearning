__author__ = 'czaOrz'

import logging

from czaSpider.czaBaseSpider.propBaseSpider import PropBaseSpider
from czaSpider.czaTools import *

logging = logging.getLogger(__name__)


class SpiderMetaClass(type):
    """
    动态加载custom_settings，未定义name则不支持custom_settings
    默认支持文件服务器，无则添加parse_item=True
    parse_item: 若定义此参看，则根据name进行动态加载custom_settings
                否则默认流程：保存、下载(文件服务器)、解析
    """

    def __new__(cls, className, bases, attrs):
        if "name" not in attrs:
            return super(SpiderMetaClass, cls).__new__(cls, className, bases, attrs)
        name = attrs.get("name")
        if "-" not in name or name.count('-') != 1:
            return super(SpiderMetaClass, cls).__new__(cls, className, bases, attrs)
        database_info = name.split('-', 1)
        if len(database_info) == 2:
            attrs["collName"], attrs["dbName"] = database_info
        custom_settings = attrs.get("custom_settings", None)
        parse_item = attrs.get("parse_item", False)
        attrs["custom_settings"] = merge_dict(get_custom_settings(name, parse_item), custom_settings)
        return super(SpiderMetaClass, cls).__new__(cls, className, bases, attrs)


class FuncBaseSpider(PropBaseSpider, metaclass=SpiderMetaClass):

    # 执行指令 #

    @classmethod
    def cza_run_spider(cls):
        if cls.author == __author__:
            os.system("scrapy crawl {}".format(cls.name))
        else:
            logging.error("Author is not czaOrz, Who are you?")
            sys.exit(0)

    @classmethod
    def run_timer_task(cls, task, *args, **kwargs):  # todo, it may seen little low
        timed_task(task, *args, **kwargs)

    # 解析部分函数 #

    def start_requests(self):
        if hasattr(self, "url"):
            url = self.url
            if url:
                yield Request(url, self.parse)
        elif hasattr(self, "urls"):
            urls = self.urls
            if urls:
                yield from [Request(url, self.parse) for url in urls]
        elif hasattr(self, "start_urls"):
            start_urls = self.start_urls
            if start_urls:
                yield from [Request(url, self.parse) for url in start_urls]
        else:
            raise ValueError("You Must Point one URL for spider")

    # 数据库操作函数 #
    def __init__(self):
        super(FuncBaseSpider, self).__init__()
        self.init_mongoDatabase()

    def init_mongoDatabase(self):
        self.mongoClient = get_mongo_client()
        if hasattr(self, "collName") and hasattr(self, "dbName"):
            self.sourceColl = self.get_source_collection(self.mongoClient)
            self.parsingColl = self.get_parsing_collection(self.mongoClient)

    def get_source_collection(self, Client):
        return Client[getattr(self, "dbName") + "-source"][getattr(self, "collName")]

    def get_parsing_collection(self, Client):
        return Client[getattr(self, "dbName") + "-parsing"][getattr(self, "collName")]
