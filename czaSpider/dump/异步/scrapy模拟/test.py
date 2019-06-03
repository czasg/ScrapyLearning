from twisted.internet import reactor, defer
from twisted.web.client import getPage
count = 0
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

import queue
Q = queue.Queue()

class Engine:
    def __init__(self):
        self._close = None
        self.max = 5
        self.crawing = []

    def get_response_callback(self, content, request):
        global count
        print("哈哈哈", count)
        self.crawing.remove(request)
        response = HttpResponse(content, request)
        result = request.callback(response)
        import types
        if isinstance(result, types.GeneratorType):
            for req in result:
                Q.put(req)

    def _next_request(self):
        global count
        count += 1
        print('222', count)
        if Q.qsize() == 0 and len(self.crawing) == 0:
            print("如果是空就走这里是吧")
            self._close.callback(None)
            return
        if len(self.crawing) >= self.max:
            print("如果达到上限了就走这里是吧")
            return
        while len(self.crawing) < self.max:
            try:
                print("我估计这里会打印4次")
                req = Q.get(block=False)
                print("我估计这里会打印3次")
                self.crawing.append(req)
                dfd = getPage(req.url.encode("utf-8"))
                print("会在这等吗")  # 不会再这等，而是一次全部执行完，一次全部加载吗，还是就是单纯的异步不等待而已
                dfd.addCallback(self.get_response_callback, req)
                dfd.addCallback(lambda _: reactor.callLater(0, self._next_request))
            except Exception:
                return

    @defer.inlineCallbacks
    def crawl(self, spider):  # 这里是第一步执行，会把所有的request推到队列中
        start_requests = iter(spider.start_requests())
        while True:
            try:
                request = next(start_requests)
                Q.put(request)
            except StopIteration:
                break
        reactor.callLater(0, self._next_request)  # 这里只是一个注册，并不直接执行 然后立即执行一次，与scrapy中的简直一模一样，任务全推进去后就开始执行，且不会  # 这里是run开启后第一个执行的
        print('111')
        self._close = defer.Deferred()  # 需要返回一个defer对象
        print('原来如此，会把这个流程走完，因为是生成器，会走到第一个yield来')
        yield self._close
        print('111-111')

class MySpider:
    start_urls = ["http://fanyi.youdao.com/","http://fanyi.youdao.com/","http://fanyi.youdao.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        print([response.text])

if __name__ == "__main__":
    spider = MySpider()  # 执行init
    _active = set()
    engine = Engine()  # 执行init
    d = engine.crawl(spider)  # 执行crawl方法，走完第一个yield方法，但是里面的defer方法等都不会执行，除非直接遇到了callback方法吗
    _active.add(d)
    dd = defer.DeferredList(_active)
    dd.addBoth(lambda _: reactor.stop())
    print('HERE END')
    reactor.run()  # 正式启动twisted
