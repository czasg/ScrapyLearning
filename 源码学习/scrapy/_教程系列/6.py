__title__ = '加入下载器管理'
from twisted.internet import defer, reactor
from twisted.web.client import getPage
from queue import Queue


class Scheduler:
    def __init__(self):
        self.mq = Queue()

    @classmethod
    def from_crawler(cls):
        return cls()

    def open(self):
        return

    def next_request(self):
        return self.mq.get(block=False)

    def enqueue_request(self, request):
        self.mq.put(request)

    def isEmpty(self):
        return self.mq.qsize() == 0


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


class Downloader:
    def __init__(self):
        self.active = set()

    @classmethod
    def from_crawler(cls):
        return cls()

    def fetch(self, request):
        def _deactivate(response):
            self.active.remove(request)
            return response

        self.active.add(request)
        dfd = getPage(request.url.encode())
        dfd.addBoth(self._process_content, request)
        return dfd.addBoth(_deactivate)

    def isEmpyt(self):
        return len(self.active) == 0

    def _process_content(self, response, request):
        return Response(response, request)


class Slot:
    def __init__(self, start_requests, nextcall, scheduler):
        self.start_requests = iter(start_requests)
        self.nextcall = nextcall
        self.scheduler = scheduler
        self.inprogress = []


class Engine:
    def __init__(self):
        self.max_pool_size = 4
        self.crawling = []
        self.slot = None
        self.running = True
        self.downloader = Downloader.from_crawler()

    @defer.inlineCallbacks
    def start(self):
        self._closewait = defer.Deferred()
        yield self._closewait

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests):
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = Scheduler.from_crawler()
        self.slot = Slot(start_requests, nextcall, scheduler)
        yield scheduler.open()
        self.slot.nextcall.schedule()

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

        if slot.start_requests is None and slot.scheduler.isEmpty() and not slot.inprogress and self.downloader.isEmpyt():
            self._closewait.callback(None)  # 原来是要回调啊

    def _next_request_from_scheduler(self, spider):
        request = self.slot.scheduler.next_request()
        if not request:
            return
        dfd = self._download(request)
        dfd.addBoth(self._handle_downloader_output, request, spider)
        dfd.addBoth(lambda _: self.slot.inprogress.remove(request))
        dfd.addBoth(lambda _: self.slot.nextcall.schedule())
        return dfd

    def _download(self, request):
        slot = self.slot
        def _on_success(response):
            assert isinstance(response, (Response, Request))
            if isinstance(response, Response):
                response.request = request
            return response

        def _on_complete(_):
            slot.nextcall.schedule()
            return _

        dwld = self.downloader.fetch(request)
        dwld.addCallbacks(_on_success)
        dwld.addBoth(_on_complete)
        return dwld

    def _handle_downloader_output(self, response, request, spider):
        request.callback(response)


class Request:
    def __init__(self, url, callback=None):
        self.url = url
        self.callback = callback


class Response:
    def __init__(self, byte_content, request):
        self.content = byte_content
        self.request = request
        self.url = request.url
        self.text = str(byte_content, encoding='utf-8')


class MySpider:
    start_urls = ['http://fanyi.youdao.com/', 'http://fanyi.youdao.com/', 'http://fanyi.youdao.com/', 'http://fanyi.youdao.com/',
                  'http://fanyi.youdao.com/', 'http://fanyi.youdao.com/', 'http://fanyi.youdao.com/', 'http://fanyi.youdao.com/']

    def start_requests(self):
        yield from (Request(url, self.parse) for url in self.start_urls)

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':
    @defer.inlineCallbacks
    def crawl():
        spider = MySpider()
        engine = Engine()
        yield engine.open_spider(spider, spider.start_requests())
        yield engine.start()
    d = crawl()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
