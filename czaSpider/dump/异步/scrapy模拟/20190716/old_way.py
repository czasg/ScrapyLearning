import _queue
from queue import Queue

from twisted.internet import reactor, defer
from twisted.web.client import getPage

mq = Queue()


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


class Engine:
    def __init__(self):
        self.close = None
        self.max = 2
        self.crawling = []

    def get_response_callback(self, content, request):
        self.crawling.remove(request)
        res = request.callback(TextResponse(content, request))

    def _next_request(self):
        if mq.qsize() == 0 and len(self.crawling) == 0:
            self.close.callback(None)
            return
        if len(self.crawling) > self.max:
            return
        while True:
            try:
                if len(self.crawling) <= self.max:
                    request = mq.get(block=False)
                    self.crawling.append(request)
                    dfd = getPage(request.url.encode('utf-8'))
                    dfd.addCallback(self.get_response_callback, request)
                    dfd.addCallback(lambda _: reactor.callLater(0, self._next_request))
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
                mq.put(request)
            except StopIteration:
                break
        reactor.callLater(0, self._next_request)
        self.close = defer.Deferred()
        yield self.close


class MySpider:
    def start_requests(self):
        url = "http://fanyi.youdao.com/"
        for i in range(10):
            yield Request(url, self.parse)

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':
    d = Engine().crawl(MySpider())
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
