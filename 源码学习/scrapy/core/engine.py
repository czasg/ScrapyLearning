"""
This is the Scrapy engine which controls the Scheduler, Downloader and Spiders.

For more information see docs/topics/architecture.rst

"""
import logging
from time import time

from twisted.internet import defer, task
from twisted.python.failure import Failure

from scrapy import signals
from scrapy.core.scraper import Scraper
from scrapy.exceptions import DontCloseSpider
from scrapy.http import Response, Request
from scrapy.utils.misc import load_object
from scrapy.utils.reactor import CallLaterOnce
from scrapy.utils.log import logformatter_adapter, failure_to_exc_info

logger = logging.getLogger(__name__)


class Slot(object):

    def __init__(self, start_requests, close_if_idle, nextcall, scheduler):
        self.closing = False
        self.inprogress = set() # requests in progress
        self.start_requests = iter(start_requests)
        self.close_if_idle = close_if_idle
        self.nextcall = nextcall
        self.scheduler = scheduler
        self.heartbeat = task.LoopingCall(nextcall.schedule)

    def add_request(self, request):
        self.inprogress.add(request)

    def remove_request(self, request):
        self.inprogress.remove(request)
        self._maybe_fire_closing()

    def close(self):
        self.closing = defer.Deferred()
        self._maybe_fire_closing()
        return self.closing

    def _maybe_fire_closing(self):
        if self.closing and not self.inprogress:
            if self.nextcall:
                self.nextcall.cancel()
                if self.heartbeat.running:
                    self.heartbeat.stop()
            self.closing.callback(None)


class ExecutionEngine(object):
    """
    有三个重要的实例化
    一、schedule
        调度器，实例化了dupefilter过滤器，然后还初始化了三个队列。
        dupefilter：过滤器，通过存储 method + url + response.body 生成sha1指纹，来进行过滤
        pqclass：一个优先级队列queuelib.PriorityQueue
        dqclass：一个FIFO队列，先进先出规则，并且通过pickle序列化了
        mqclass：一个FIFO队列，先进先出规则，直接存储在内存中

    二、downloader
        实例化了Handler对象，还实例化了下载器中间件
        Handler：具体的下载逻辑
        DownloaderMiddlewareManager：收集所有的下载中间件，在收集其中的process_request、process_exception、process_response三种方法

    三、scraper
        实例化了爬虫中间件，还实例化了管道处理器
        SpiderMiddlewareManager：实例化后获取process_spider_input、process_spider_output、process_spider_exception、process_start_requests
        itemproc_cls：获取ItemPipelineManager，实例化其中的ITEM_PIPELINES，获取process_item

    """
    def __init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self.settings = crawler.settings
        self.signals = crawler.signals
        self.logformatter = crawler.logformatter
        self.slot = None
        self.spider = None
        self.running = False
        self.paused = False
        self.scheduler_cls = load_object(self.settings['SCHEDULER'])  # SCHEDULER = 'scrapy.core.scheduler.Scheduler'，仅仅获取对象，没做其他坏事
        downloader_cls = load_object(self.settings['DOWNLOADER'])  # DOWNLOADER = 'scrapy.core.downloader.Downloader'
        self.downloader = downloader_cls(crawler)  # 这个下载器，里面实例化了handler处理器，和到下载器之间的process_处理逻辑。就是具体的下载功能和中间件功能都已经实现了
        self.scraper = Scraper(crawler)  # 这里有定义有spidermw爬虫中间件和ITEM_pipeline管道对象，数据处理功能和存储功能都实现了
        self._spider_closed_callback = spider_closed_callback  # 这个回调很重要，关系到爬虫能不能停下来，是个匿名函数lambda _: self.stop()，最终还是执行engine的self.engine.stop

    @defer.inlineCallbacks
    def start(self):
        """Start the execution engine"""
        assert not self.running, "Engine already running"
        self.start_time = time()
        yield self.signals.send_catch_log_deferred(signal=signals.engine_started)
        self.running = True
        self._closewait = defer.Deferred()
        yield self._closewait

    def stop(self):
        """Stop the execution engine gracefully"""
        assert self.running, "Engine not running"
        self.running = False
        dfd = self._close_all_spiders()
        return dfd.addBoth(lambda _: self._finish_stopping_engine())

    def close(self):
        """Close the execution engine gracefully.

        If it has already been started, stop it. In all cases, close all spiders
        and the downloader.
        """
        if self.running:
            # Will also close spiders and downloader
            return self.stop()
        elif self.open_spiders:
            # Will also close downloader
            return self._close_all_spiders()
        else:
            return defer.succeed(self.downloader.close())

    def pause(self):
        """Pause the execution engine"""
        self.paused = True

    def unpause(self):
        """Resume the execution engine"""
        self.paused = False

    def _next_request(self, spider):
        slot = self.slot
        if not slot:
            return

        if self.paused:
            return

        while not self._needs_backout(spider):  # 什么时候才会出来呢??
            """首次执行状态
            True False False False
            """
            # 当爬虫running为True
            # 心跳关闭slot.closing=True
            # 下载器有active活跃数量大于16
            # 刮擦有active活跃数量大于5000000
            if not self._next_request_from_scheduler(spider):  # 就是加入这里我放了10个函数呢
                """
                会一直递归获取所有的request，丢到下载器进行下载，最后一步为经历了scraper的润色
                
                从调度器中pop出一个request请求
                执行下载函数，获取结果，如果是request则继续入队，并递归心跳函数，否则继续往下走
                执行对结果的处理
                
                居然会在start_requests之前执行，不可思议，存在记录的话最少要走两次，一次走完，还有一次走结束
                
                执行_next_request_from_scheduler
                Done!  首次直接走掉，应为队列里面一个数据都没有
                
                然后从start_requests里面next出一个数据，推到队列面去，所以数据怎么进去，居然是一个一个next出来推进去的，那个百度小哥着实牛逼
                """
                break

        if slot.start_requests and not self._needs_backout(spider):
            try:
                request = next(slot.start_requests)  # 数据就是从这里，一个一个的从start_requests调出来然后再推进去的，神奇的异步
            except StopIteration:
                slot.start_requests = None
            except Exception:
                slot.start_requests = None
                logger.error('Error while obtaining start requests',
                             exc_info=True, extra={'spider': spider})
            else:
                """
                所以我感觉现在的情况就很尴尬，我刚往里面push一个数据，然后继续调用时，又立马给我pop出来了，真是醉了
                """
                self.crawl(request, spider)

        if self.spider_is_idle(spider) and slot.close_if_idle:
            self._spider_idle(spider)

    def _needs_backout(self, spider): # len(self.active) >= self.total_concurrency # return self.active_size > self.max_active_size
        slot = self.slot
        return not self.running \
            or slot.closing \
            or self.downloader.needs_backout() \
            or self.scraper.slot.needs_backout()

    def _next_request_from_scheduler(self, spider):  # 怎么感觉这一个函数就可以把所有流程走完啊???????
        slot = self.slot
        request = slot.scheduler.next_request()  # 从调度器中pop出一条request记录
        if not request:
            return
        d = self._download(request, spider)
        d.addBoth(self._handle_downloader_output, request, spider)
        d.addErrback(lambda f: logger.info('Error while handling downloader output',
                                           exc_info=failure_to_exc_info(f),
                                           extra={'spider': spider}))
        d.addBoth(lambda _: slot.remove_request(request))
        d.addErrback(lambda f: logger.info('Error while removing request from slot',
                                           exc_info=failure_to_exc_info(f),
                                           extra={'spider': spider}))
        d.addBoth(lambda _: slot.nextcall.schedule())
        d.addErrback(lambda f: logger.info('Error while scheduling new request',
                                           exc_info=failure_to_exc_info(f),
                                           extra={'spider': spider}))
        return d

    def _handle_downloader_output(self, response, request, spider):  # 这里链接到download下载后的response
        assert isinstance(response, (Request, Response, Failure)), response
        # downloader middleware can return requests (for example, redirects)
        if isinstance(response, Request): # 对于结果，如果是Request，则直接入队，进入self.crawl
            self.crawl(response, spider)  # 对request请求指纹过滤，没问题则入队，然后递归心跳处理
            return
        # response is a Response or Failure
        d = self.scraper.enqueue_scrape(response, request, spider)  # 如果是正确的response，对下载器输出的结果进行scraper的三个处理函数，如果结果是request继续入队，如果是字典或者Item则调用process_item函数进行后续处理
        d.addErrback(lambda f: logger.error('Error while enqueuing downloader output',
                                            exc_info=failure_to_exc_info(f),
                                            extra={'spider': spider}))
        return d

    def spider_is_idle(self, spider):  # 爬虫 闲置 状态 ??
        if not self.scraper.slot.is_idle():  # scraper处于闲置
            # scraper is not idle
            return False

        if self.downloader.active:  # 下载器处于闲置
            # downloader has pending requests
            return False

        if self.slot.start_requests is not None:  # 所有start_requests处于空
            # not all start requests are handled
            return False

        if self.slot.scheduler.has_pending_requests():  # 调度器 所有等待任务 为空
            # scheduler has pending requests
            return False

        return True  # 判断闲置的四个条件：start_requests、调度器、下载器、scraper均闲置，才会判断爬虫处于闲置状态。

    @property
    def open_spiders(self):
        return [self.spider] if self.spider else []

    def has_capacity(self):
        """Does the engine have capacity to handle more spiders"""
        return not bool(self.slot)

    def crawl(self, request, spider):  # 将请求进行指纹过滤，没问题则入队，然后递归执行心跳
        assert spider in self.open_spiders, \
            "Spider %r not opened when crawling: %s" % (spider.name, request)
        self.schedule(request, spider)
        self.slot.nextcall.schedule()  # 又执行一次

    def schedule(self, request, spider):
        self.signals.send_catch_log(signal=signals.request_scheduled,
                request=request, spider=spider)
        if not self.slot.scheduler.enqueue_request(request):  # 什么是否才会走到这里呢 - 请求指纹过滤，若没有过滤掉，则入队，self._dqpush(request)也就是push进队列
            self.signals.send_catch_log(signal=signals.request_dropped,
                                        request=request, spider=spider)

    def download(self, request, spider):
        d = self._download(request, spider)
        d.addBoth(self._downloaded, self.slot, request, spider)
        return d

    def _downloaded(self, response, slot, request, spider):  # 下载结束时，心跳中移除请求
        slot.remove_request(request)
        return self.download(response, spider) \
                if isinstance(response, Request) else response  # 是Request则继续调用上面函数

    def _download(self, request, spider):
        slot = self.slot
        slot.add_request(request)
        def _on_success(response):  # 如果是response，就是正常的response对象了，但是应该还没有进行回调处理吧
            assert isinstance(response, (Response, Request))
            if isinstance(response, Response):
                response.request = request # tie request to response received
                logkws = self.logformatter.crawled(request, response, spider)
                logger.log(*logformatter_adapter(logkws), extra={'spider': spider})
                self.signals.send_catch_log(signal=signals.response_received, \
                    response=response, request=request, spider=spider)
            return response

        def _on_complete(_):
            slot.nextcall.schedule()
            return _

        dwld = self.downloader.fetch(request, spider)  # 爬虫下载入口，调用middle进行下载，把真正的下载函数传递过滤，在middle中间进行回调的时候，处理第一个管道，没了再执行下载器进行处理
        dwld.addCallbacks(_on_success)
        dwld.addBoth(_on_complete)
        return dwld

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=(), close_if_idle=True):
        assert self.has_capacity(), "No free spider slot when opening %r" % \
            spider.name
        logger.info("Spider opened", extra={'spider': spider})
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_cls.from_crawler(self.crawler)  # 对调度器进行实例化。实例化了dupefilter，还有三种队列。一种是优先级队列，还有来两个都是fifo先进先出队列，不过一个是直接存储在内存memory中，一个是通过pickle实例化了
        start_requests = yield self.scraper.spidermw.process_start_requests(start_requests, spider)  # 第一步执行的居然是爬虫中间件里面的process_start_requests
        slot = Slot(start_requests, close_if_idle, nextcall, scheduler)
        self.slot = slot
        self.spider = spider
        yield scheduler.open(spider)  # 打开内存队列FIFO，优先级队列，并打开过滤器
        yield self.scraper.open_spider(spider)  # 貌似没做啥事
        self.crawler.stats.open_spider(spider)  # pass，也没做啥事
        yield self.signals.send_catch_log_deferred(signals.spider_opened, spider=spider)  # 做了好多事啊，初始化日志，还有各种装啊提，中间件似乎都实现了这个函数?
        slot.nextcall.schedule()  # 执行一次self._next_request
        # 这鬼地方居然只会走一次，也就是初始化的走完这里，但是并不会执行里面的逻辑，应为这个schedule里面用的是reactor.callLater(delay, self)，所以是不会执行的，除非你start
        slot.heartbeat.start(5)

    def _spider_idle(self, spider):
        """Called when a spider gets idle. This function is called when there
        are no remaining pages to download or schedule. It can be called
        multiple times. If some extension raises a DontCloseSpider exception
        (in the spider_idle signal handler) the spider is not closed until the
        next loop and this function is guaranteed to be called (at least) once
        again for this spider.
        """
        res = self.signals.send_catch_log(signal=signals.spider_idle, \
            spider=spider, dont_log=DontCloseSpider)
        if any(isinstance(x, Failure) and isinstance(x.value, DontCloseSpider) \
                for _, x in res):
            return

        if self.spider_is_idle(spider):
            self.close_spider(spider, reason='finished')

    def close_spider(self, spider, reason='cancelled'):
        """Close (cancel) spider and clear all its outstanding requests"""

        slot = self.slot
        if slot.closing:
            return slot.closing
        logger.info("Closing spider (%(reason)s)",
                    {'reason': reason},
                    extra={'spider': spider})

        dfd = slot.close()

        def log_failure(msg):
            def errback(failure):
                logger.error(
                    msg,
                    exc_info=failure_to_exc_info(failure),
                    extra={'spider': spider}
                )
            return errback

        dfd.addBoth(lambda _: self.downloader.close())
        dfd.addErrback(log_failure('Downloader close failure'))

        dfd.addBoth(lambda _: self.scraper.close_spider(spider))
        dfd.addErrback(log_failure('Scraper close failure'))

        dfd.addBoth(lambda _: slot.scheduler.close(reason))
        dfd.addErrback(log_failure('Scheduler close failure'))

        dfd.addBoth(lambda _: self.signals.send_catch_log_deferred(
            signal=signals.spider_closed, spider=spider, reason=reason))
        dfd.addErrback(log_failure('Error while sending spider_close signal'))

        dfd.addBoth(lambda _: self.crawler.stats.close_spider(spider, reason=reason))
        dfd.addErrback(log_failure('Stats close failure'))

        dfd.addBoth(lambda _: logger.info("Spider closed (%(reason)s)",
                                          {'reason': reason},
                                          extra={'spider': spider}))

        dfd.addBoth(lambda _: setattr(self, 'slot', None))
        dfd.addErrback(log_failure('Error while unassigning slot'))

        dfd.addBoth(lambda _: setattr(self, 'spider', None))  # 这里有点意思
        dfd.addErrback(log_failure('Error while unassigning spider'))

        dfd.addBoth(lambda _: self._spider_closed_callback(spider))

        return dfd

    def _close_all_spiders(self):
        dfds = [self.close_spider(s, reason='shutdown') for s in self.open_spiders]
        dlist = defer.DeferredList(dfds)
        return dlist

    @defer.inlineCallbacks
    def _finish_stopping_engine(self):
        yield self.signals.send_catch_log_deferred(signal=signals.engine_stopped)
        self._closewait.callback(None)
