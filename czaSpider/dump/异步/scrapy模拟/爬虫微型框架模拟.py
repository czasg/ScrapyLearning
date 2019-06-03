__goal__ = "Simulate Scrapy For Spider"
"""
引擎：
调度器：
下载器：一个比较核心的模块，建立在twisted模块上
爬虫：解析出item或者request
项目管道：
下载中间件：process_request(request, spider)/process_response(request, response, spider)
爬虫中间件：
调度中间件：

大致流程：
引擎从调度器中获取URL，兵封装成Request请求传入下载器
下载器把资源下载好后，封装成Response结果传入爬虫
爬虫解析Response
此时可以获取两种结果，一种为Item，一种为Request，前者则进入管道进行序列化处理，后者则进度调度器
"""

from twisted.internet import defer, reactor
from twisted.web.client import Agent, ProxyAgent, ResponseDone, HTTPConnectionPool, ResponseFailed, getPage
from treq import get

class Request:
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback

class HttpResponse:
    def __init__(self, content, request):
        self.content = content
        self.request = request
        self.url = request.url
        self.text = str(content, encoding="utf-8")

class MySpider:
    name = "test"
    start_urls = ["http://fanyi.youdao.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        print(response.request)
        print(response.url)

import queue
Q = queue.Queue()

class Engine:
    def __init__(self):
        self._close = None
        self.max = 5
        self.crawing = []

    def get_response_callback(self, content, request):
        self.crawing.remove(request)
        req = HttpResponse(content, request)
        res = request.callback(req)
        import types
        if isinstance(res, types.GeneratorType):
            for req in res:
                Q.put(req)

    def _next_request(self):
        if Q.qsize() == 0 and len(self.crawing) == 0:
            self._close.callback(None)
            return

        if len(self.crawing) >= self.max:
            return

        while len(self.crawing) < self.max:
            try:
                req = Q.get(block=False)
                self.crawing.append(req)
                # dfd = get(req.url.encode("utf-8"))
                dfd = getPage(req.url.encode("utf-8"))
                dfd.addCallback(self.get_response_callback, req)
                dfd.addCallback(lambda _: reactor.callLater(0, self._next_request))
            except:
                return

    @defer.inlineCallbacks
    def crawl(self, spider):
        start_requests = iter(spider.start_requests())
        while True:
            try:
                request = next(start_requests)
                Q.put(request)
            except StopIteration:
                break
        reactor.callLater(0, self._next_request)
        self._close = defer.Deferred()
        yield self._close

spider = MySpider()
_active = set()
engine = Engine()
dfd = engine.crawl(spider)
_active.add(dfd)
d = defer.DeferredList(_active)
d.addBoth(lambda _: reactor.stop())
reactor.run()

