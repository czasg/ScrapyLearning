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
    def __init__(self):
        self.mq = Queue()

    @classmethod
    def open_spider(cls):
        return cls()

    def next_request(self):
        return self.mq.get(block=False)

    def enqueue_request(self, request):
        self.mq.put(request)

    def isEmpty(self):
        return self.mq.qsize() == 0


class Downloader:
    def __init__(self):
        self.active = set()

    @classmethod
    def from_crawler(cls):
        return cls()

    def start_download(self, request):
        def _delActive(response):
            self.active.remove(request)
            return response
        self.active.add(request)
        d = getPage(request.url.encode('utf-8'))
        d.addBoth(_delActive)
        d.addBoth(self._process_content, request)
        return d

    def isEmpyt(self):
        return len(self.active) == 0

    def _process_content(self, content, request):
        return TextResponse(content, request)


class Scraper:
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


"""Crawler/CrawlerRunner/CrawlerProcess"""


class Crawler:
    def __init__(self, spider_cls):
        self.spider_cls = spider_cls
        self.engine = None

    @defer.inlineCallbacks
    def crawl(self):
        self.spider_cls = self.spider_cls.from_crawler()  # 实例化用户定义的爬虫
        self.engine = Engine.from_crawler(self)
        start_requests = iter(self.spider_cls.start_requests())
        yield self.engine.open_spider(self.spider_cls, start_requests)
        yield self.engine.start()


class CrawlerRunner:
    def __init__(self):
        self.crawling = []
        self._active = []

    def crawl(self, spider):
        crawler = Crawler(spider)  # 实例化当前爬虫，封装为Crawler对象
        return self._crawl(crawler)

    def _crawl(self, crawler):
        self.crawling.append(crawler)
        d = crawler.crawl()  # 返回defer对象
        self._active.append(d)

        def _done(result):  #
            self.crawling.remove(result)
            self._active.remove(result)
            return result

        d.addBoth(_done)
        return d


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

    def cancel(self):
        if self._call:
            self._call.cancel()

    def __call__(self, *args, **kwargs):
        self._call = None
        return self.func(*self.args, **self.kwargs)


class Slot:
    def __init__(self, start_requests, nextcall, scheduler):
        self.start_requests = iter(start_requests)
        self.nextcall = nextcall
        self.scheduler = scheduler
        self.inprogress = []


class Engine:
    def __init__(self, crawler):
        self.crawler = crawler
        self.close = None
        self.max = 2
        self.slot = None
        self.downloader = Downloader.from_crawler()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    @defer.inlineCallbacks
    def start(self):  # 在结束的地方调用callback
        self.close = defer.Deferred()
        yield self.close

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests):
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = Schedule.open_spider()
        self.slot = Slot(start_requests, nextcall, scheduler)
        yield
        self.slot.nextcall.schedule()  # 首次这里应该是不执行把???

    def _next_request(self, spider):
        slot = self.slot
        if not slot:
            return

        while not slot.scheduler.isEmpty():
            if not self._next_request_from_scheduler(spider):
                break

        if slot.start_requests:
            try:
                request = next(slot.start_requests)
                slot.inprogress.append(request)
            except StopIteration:
                slot.start_requests = None
            else:
                slot.scheduler.enqueue_request(request)
                slot.nextcall.schedule()

        if slot.start_requests is None and slot.scheduler.isEmpty() and self.downloader.isEmpyt():
            self.close.callback(None)  # 原来是要回调啊

    def _next_request_from_scheduler(self, spider):
        request = self.slot.scheduler.next_request()
        if not request:
            return
        dfd = self.downloader.start_download(request)
        dfd.addBoth(self._handle_downloader_output, request, spider)
        dfd.addBoth(lambda _: self.slot.inprogress.remove(request))
        dfd.addBoth(lambda _: self.slot.nextcall.schedule())
        return dfd

    def _handle_downloader_output(self, response, request, spider):  # 传进来的居然是一个None???
        print(response.url)
        print(len(self.slot.inprogress))
        d = defer.Deferred()
        d.callback(None)
        return d


class MySpider(Spider):
    def start_requests(self):
        url = "http://fanyi.youdao.com/"
        for i in range(10):
            yield Request(url, self.parse)

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':  # todo, 怎么停下来，是一个问题
    import time
    start_time = time.time()
    o = CrawlerProcess()
    d = o.crawl(MySpider)
    d.addBoth(lambda _: reactor.stop())
    o.start()

    # import requests
    # for i in range(10):
    #     print(requests.get("http://fanyi.youdao.com/").url)

    end_time = time.time()
    print(end_time - start_time)
