__author__ = "czaOrz"

"""
通过在scrapy命令行中输入-s key=value，则可以在爬虫中使用self.crawler.settings.get("key")的方式获取

scrapy中response.request就是代表一个Request对象，且是上一级的请求对象。而response.request.callback则是指接受此response对象的函数




"""