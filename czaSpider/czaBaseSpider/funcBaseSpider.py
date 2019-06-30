__author__ = 'czaOrz'

import logging
import traceback

from threading import Thread
from scrapy.http import TextResponse

from czaSpider.czaBaseSpider.propBaseSpider import PropBaseSpider
from czaSpider.dataBase.mysql_database.orm import get_mysql_connection
from czaSpider.dataBase.mongo_database.models import Mongodb
from czaSpider.dataBase.file_database.downloader import Downloader
from czaSpider.dataBase.file_database.fileManager import FileManager
from czaSpider.czaTools import *
from czaSpider import items

logger = logging.getLogger(__name__)


class SpiderMetaClass(type):
    """
    ---动态加载---
    需定义name，若未定义name或定义异常name则不支持此功能。动态加载对象：dbName|collName|mongo|custom_settings
    dbName: mongodb数据库
    collName: mongodb集合库
    mongo: mongodb对象，包含source和resolver两种库
    custom_settings: 自定义中间件，默认强制使用sourcePipeline，可使用parse_item解除

    ---parse_item---
    爬虫的下载与解析，默认需要文件服务器支持，若无文件服务器
    可添加parse_item=True参数，使用原生scrapy中间件进行解析，此处支持动态加载
    parse_item: 若定义此参数，则根据name进行动态加载custom_settings
                否则默认流程为：保存、下载(文件服务器)、解析(sourcePipeline)
    """

    def __new__(cls, className, bases, attrs):
        if "name" not in attrs:
            return super(SpiderMetaClass, cls).__new__(cls, className, bases, attrs)
        name = attrs.get("name")
        if "-" not in name or name.count('-') != 1:
            return super(SpiderMetaClass, cls).__new__(cls, className, bases, attrs)

        # dynamic loading
        collName, dbName = name.split('-', 1)
        custom_settings = attrs.get("custom_settings", None)
        parse_item = attrs.get("parse_item", False)
        attrs["collName"] = collName
        attrs["dbName"] = dbName
        attrs["mongo"] = Mongodb(dbName, collName, parse_item)
        attrs["custom_settings"] = merge_dict(get_custom_settings(name, parse_item), custom_settings)
        return super(SpiderMetaClass, cls).__new__(cls, className, bases, attrs)


class FuncBaseSpider(PropBaseSpider, metaclass=SpiderMetaClass):

    # 执行指令 #

    @classmethod
    def cza_run_spider(cls):  # todo, subprocess packages?
        os.system("scrapy crawl {}".format(cls.name))

    @classmethod
    def mongodb2csv(cls, source=False, resolver=False):
        mongodb2csv(cls, source, resolver)

    @classmethod
    def file_download(cls, thread=1, delay=0, tolerate=6):
        cls._file_download(thread, delay, tolerate)

    @classmethod
    def file_parse(cls, thread=1):
        cls._file_parse(thread)

    @classmethod
    def file_reParse(cls, thread=1):
        cls._file_reParse(thread)

    # 初始化部分 #

    def __init__(self):
        super(FuncBaseSpider, self).__init__()
        self.init_mysqlDatabase()

    def init_mysqlDatabase(self):
        if hasattr(self, 'allow_mysql') and hasattr(self, 'dbName'):
            from czaSpider.dataBase.mysql_database import models
            mysql_dbName = '%sDB' % self.dbName
            if hasattr(models, mysql_dbName):
                if get_mysql_connection():  # todo, exist BUG! can not connect MySQL, WHY?!
                    self.mysql = getattr(models, mysql_dbName)

    # 文件下载部分 #

    @classmethod
    def _file_download(cls, thread=1, delay=0, tolerate=6):
        downloader = Downloader(cls,
                                thread=thread,
                                delay=delay,
                                tolerate=tolerate,
                                allow_download_fail=cls.ALLOW_DOWNLOAD_FAIL)
        downloader.start()

    # 数据解析部分 #

    def start_requests(self):
        yield from [Request(self.url, self.parse)] if self.url else [Request(url, self.parse) for url in self.urls]

    def process_item(self, **kwargs):
        func = None
        if getattr(self, "parse_item"):
            if hasattr(items, self.dbName + "Item"):
                func = getattr(items, self.dbName + "Item")
        func = func if func else getattr(items, "sourceItem")
        return func(**kwargs)

    # 文件解析部分 #

    @classmethod
    def _file_parse(cls, thread=1):
        logger.warning('start parsing...')
        threads = [Thread(target=cls._file_parse_further, args=(thread, index, None)) for index in range(thread)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        logger.warning('parsing done!')

    @staticmethod
    def _thread_filter(thread, index, document):
        return thread > 1 and not ord(str(document["_id"])[-1]) % thread == index

    @classmethod
    def _file_parse_further(cls, thread=1, index=None, callback=None):
        documents = cls.mongo.source.findAll(download_finished=True, parse_time=None, **cls.parse_filter).documents
        for document in documents:
            if cls._thread_filter(thread, index, document):
                continue
            try:
                response = cls._process_document(document)
                info = document.pop("more", {})
                callback(response, document, info) if callback else cls._parse_detail(response, document, info)
            except:
                logger.error(traceback.format_exc())
                logger.error(str(document))

    @classmethod
    def _process_document(cls, document):
        response = [cls._process_source(source, document) for source in document['source']]
        return response[0] if len(response) == 1 else response

    @classmethod
    def _process_source(cls, source, document):
        return TextResponse(url=cls._url_from_source(source, document),
                            body=FileManager(**source).fetch_file(),
                            encoding=cls.PARSE_ENCODING)

    @classmethod
    def _url_from_source(cls, source, document):
        return source['request']['url'] if isinstance(source['request'], dict) else document['url']

    @classmethod
    def _parse_detail(cls, response, document, info):
        documents = [item.copy() for item in cls.process_detail(response, document, info)]
        cls.mongo.resolver.insertAll(cls._polish_outputs(documents)) if documents else None
        cls.mongo.source.update(_id=document['_id'], set={'parse_time': datetime.datetime.now()})

    @classmethod
    def process_detail(cls, response, document, info):
        raise Exception()

    @classmethod
    def _polish_outputs(cls, documents: list) -> list:
        return documents

    @classmethod
    def _file_reParse(cls, thread):
        cls.mongo.source.updateAll(set={"parse_time": None})
        cls.mongo.resolver.drop()
        cls.file_parse(thread)

    # test for asynchronous parsing - Failure #

    @classmethod
    def test(cls):
        cls.mongo.source.updateAll(set={"parse_time": None})
        cls.mongo.resolver.drop()
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cls._test1(loop))
        loop.stop()

    @classmethod
    async def _test1(cls, loop):
        documents = cls.mongo.source.findAll(download_finished=True, parse_time=None, **cls.parse_filter).documents
        for document in documents:
            try:
                response = cls._process_document(document)
                info = document.pop("more", {})
                cls._test3(response, document, info, loop)
            except:
                logger.error(traceback.format_exc())
                logger.error(str(document))

    @classmethod
    def _test3(cls, response, document, info, loop):
        documents = [item.copy() for item in cls.process_detail(response, document, info)]
        loop.run_in_executor(None, cls.future, documents, document)

    @classmethod
    def future(cls, documents, document):
        cls.mongo.resolver.insertAll(cls._polish_outputs(documents)) if documents else None
        cls.mongo.source.update(_id=document['_id'], set={'parse_time': datetime.datetime.now()})
