import logging

from czaSpider.czaTools import *
from czaSpider import items

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class czaSpider(scrapy.Spider):
    name = "czaSpider"
    author = "czaOrz"
    collName = ""
    dbName = ""

    ITEM_SOURCE = False
    SQLITE3 = False

    def __init__(self):
        super(czaSpider, self).__init__()
        # self.init_db_setting()
        # self.mongoClient = get_mongo_client()
        # self.collection = self.get_collection(self.mongoClient)
        # self.sqlite3Conn = get_sqlite3_connection()
        # self.redisClient = get_redis_client()

    @classmethod
    def get_collection(cls, client, dbName=None):
        dbName = dbName if dbName else get_database_name(cls.name)
        return client[dbName][cls.collName]

    def start_requests(self):
        log.info("spider start...")
        if hasattr(self, "cza_start_request"):
            yield from self.cza_start_request()
            return
        if hasattr(self, "url"):
            url = self.url
            if url:
                yield Request(url, self.parse)
            else:
                raise ValueError("Please input a effective url")
        else:
            raise ValueError("Please define a url for spider, like url=xxx")

    @classmethod
    def process_item(cls, **kwargs):
        kwargs.setdefault("spiderName",cls.name)
        kwargs.setdefault("author", cls.author)
        if cls.ITEM_SOURCE:
            return getattr(items, constant.SAVED_SOURCE_NAME)(**kwargs)

        itemName = cls.name[cls.name.rfind('-') + 1:] + "Item"
        return getattr(items, itemName)(**kwargs)

    @classmethod
    def cza_run_spider(cls):
        if cls.author == "czaOrz":
            os.system("scrapy crawl {}".format(cls.name))
        else:
            log.error("auther is not czaOrz, Who are you?")
            sys.exit(0)

    @classmethod
    def run_timer_task(cls, task, *args, **kwargs):
        timed_task(task, *args, **kwargs)

    @classmethod
    def init_db_setting(cls, timeStr=True):
        if cls.SQLITE3:  # only save source
            cls.sqlite3Conn = get_sqlite3_connection(timeStr=True)  # cursor
            execute_sql(cls.sqlite3Conn, constant.SQL_CREATE_TABLE)

        cls.mongoClient = get_mongo_client()
        if cls.ITEM_SOURCE:
            cls.collName = get_collection_name(constant.SOURCE, timeStr=timeStr)
            cls.collection = cls.get_collection(cls.mongoClient, constant.SOURCE)
            cls.dbName = get_database_name(cls.name)
            return
        cls.collName = get_collection_name(cls.name, timeStr=timeStr)
        cls.collection = cls.get_collection(cls.mongoClient)
        cls.dbName = get_database_name(cls.name)


    @classmethod
    def processDataFromDatabase(cls):
        pass


