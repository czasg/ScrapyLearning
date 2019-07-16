from twisted.internet import reactor, defer
from twisted.web.client import getPage
from queue import Queue

"""Spider/Request/Response"""
class Spider:
    @classmethod
    def from_crawler(cls):
        return cls()

class Request:
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback

class TextResponse:
    def __init__(self, content, request):
        self.content = content
        self.request = request
        self.url = request.url
        self.text = str(content, encoding='utf-8')

"""Schedule"""
class Schedule:
    def __init__(self, spider):
        self.spider = spider
        self.mp = Queue()

    @classmethod
    def open_spider(cls, spider):
        return cls(spider)

    def check_stop(self):
        return self.mp.qsize() == 0

"""Crawler/CrawlerRunner/CrawlerProcess"""
class Crawler:
    def __init__(self, spider_cls):
        self.spider_cls = spider_cls
        self.engine = None

    @defer.inlineCallbacks
    def crawl(self):
        self.spider_cls = self.spider_cls.from_crawler()
        self.engine = Engine.from_crawler(self)
        start_requests = iter(self.spider_cls.start_requests())
        yield self.engine.open_spider(self.spider_cls, start_requests)
        yield self.engine.start()

class CrawlerRunner:
    def __init__(self):
        self.crawling = []
        self._active = []

    def crawl(self, spider):
        crawler = Crawler(spider)
        return self._crawl(crawler)

    def _crawl(self, crawler):
        self.crawling.append(crawler)
        d = crawler.crawl()
        self._active.append(d)
        def _done(result):
            self.crawling.remove(result)
            self._active.remove(result)
            return result
        return d.addBoth(_done)

class CrawlerProcess(CrawlerRunner):
    def __init__(self):
        super(CrawlerProcess, self).__init__()

    def start(self):
        reactor.run()


""""""
class CallLaterOnce:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._call = None

    def schedule(self):
        if self._call is None:
            self._call = reactor.callLater(0, self)

    def __call__(self, *args, **kwargs):
        self._call = None
        return self.func(*self.args, **self.kwargs)


class Slot:
    def __init__(self,start_requests, nextcall, scheduler):
        self.start_requests = start_requests
        self.nextcall = nextcall
        self.scheduler = scheduler

class Engine:
    def __init__(self, crawler):
        self.crawler = crawler
        self.close = None
        self.max = 2
        self.slot = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    @defer.inlineCallbacks
    def start(self):
        self.close = defer.Deferred()
        yield self.close

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests):
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = Schedule.open_spider(spider)
        self.slot = Slot(start_requests, nextcall, scheduler)
        self.slot.nextcall.schedule()

    def _next_request(self, spider):
        if self.slot.scheduler.check_stop():
            # self.close.callback(None)
            print(self.close)
            return

class MySPider(Spider):
    def start_requests(self):
        url = "http://fanyi.youdao.com/"
        yield Request(url, self.parse)

    def parse(self, response):
        print(response.url)

if __name__ == '__main__':
    o = CrawlerProcess()
    o.crawl(MySPider)
    o.start()
