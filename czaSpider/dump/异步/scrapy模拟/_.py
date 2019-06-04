from twisted.internet import reactor, defer
from twisted.web.client import getPage
from queue import Queue

Q = Queue()

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

class Engine:
    def __init__(self):
        self._close = None
        self.max = 2
        self.crawling = []

    def get_response_callback(self, content, request):
        self.crawling.remove(request)
        res = request.callback(HttpResponse(content, request))
        import types
        if isinstance(res, types.GeneratorType):
            for r in res:
                if isinstance(r, Request):
                    Q.put(r)

    def _next_request(self):
        if Q.qsize() == 0 and len(self.crawling) == 0:
            self._close.callback(None)
            return
        if len(self.crawling) > self.max:
            return
        import _queue
        while True:
            try:
                if len(self.crawling) <= self.max:
                    # print("这里会打印三次呢")
                    request = Q.get(block=False)
                    self.crawling.append(request)
                    d = getPage(request.url.encode("utf-8"))
                    d.addCallback(self.get_response_callback, request)
                    d.addCallback(lambda _: reactor.callLater(0, self._next_request))
                else:
                    break
            except _queue.Empty:
                break

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

class MySpider:
    start_urls = ["http://fanyi.youdao.com/","http://fanyi.youdao.com/",
                  "http://fanyi.youdao.com/",]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        print([response.text])
        yield Request(url="http://fanyi.youdao.com/", callback=self.parse)

if __name__ == "__main__":
    d = Engine().crawl(MySpider())
    d.addBoth(lambda _: reactor.stop())
    reactor.run()