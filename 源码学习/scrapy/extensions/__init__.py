__file__ = 'extensions'

"""拓展模块
拓展模块，并不属于中间件把

需要定义from_crawler函数老实例化一个拓展类对象，一般是根据signal信号进行控制

"""

"""
closespider：关闭爬虫，设定一个关闭的条件，与相关signal进行绑定，一旦触发此条件，直接调用self.crawler.engine.close_spider(spider, 'closespider_errorcount')进行关闭

"""
