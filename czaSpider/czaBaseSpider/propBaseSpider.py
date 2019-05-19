import scrapy

"""
爬虫属性默认清单，有需要请自行覆盖

"""


class PropBaseSpider(scrapy.Spider):
    # 爬虫属性 #
    name = "IOCO"
    url = None
    urls = None
    parse_item = False  # 是否使用原生scrapy中间件解析

    # 动态加载属性 #
    mongo = None
    dbName = None
    collName = None
    custom_settings = None

    # 下载配置项 #
    ALLOW_DOWNLOAD_FAIL = False  # 允许下载不成功导致的异常

    # 解析配置项 #
    parse_filter = {}  # 指定mongodb中的数据进行过滤，默认为所有数据
    PARSE_ENCODING = 'utf-8'  # 指定解析过程使用的编码，默认utf-8
