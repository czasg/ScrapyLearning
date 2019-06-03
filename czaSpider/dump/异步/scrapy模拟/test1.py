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
        self.max = 5
        self.crawing = []

    def get_response_callback(self, content, request):
        self.crawing.remove(request)
        response = HttpResponse(content, request)
        res = request.callback(response)
        import types
        if isinstance(res, types.GeneratorType):
            for r in res:
                Q.put(r) if isinstance(r, Request) else None

    def _next_request(self):
        if Q.qsize() == 0 and len(self.crawing) == 0:
            self._close.callback(None)
            return
        if len(self.crawing) > self.max:
            return
        while len(self.crawing) < self.max:
            try:
                req = Q.get(block=False)
                self.crawing.append(req)
                d = getPage(req.url.encode("utf-8"))
                d.addCallback(self.get_response_callback, req)
                d.addCallback(lambda _: reactor.callLater(0, self._next_request))
            except Exception:
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

class MySpier:
    start_urls = ["http://fanyi.youdao.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        print([response.text])

if __name__ == "__main__":
    spider = MySpier()
    engine = Engine()
    d = engine.crawl(spider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
