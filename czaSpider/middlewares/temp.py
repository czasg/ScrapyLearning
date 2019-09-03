from scrapy import signals
from twisted.internet import task

class TimeExecuter:
    task = None

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getint('INTERVAL_EXECUTE', 300)
        return cls(interval=interval, crawler=crawler)

    def __init__(self, interval, crawler):
        self.interval = interval
        self.stats = crawler.stats
        self.crawler = crawler
        self.count_cache = 0
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):  # 每当爬虫开始执行的时候就运行，挂起一个loop
        self.task = task.LoopingCall(self.check_shutdown, spider)
        self.task.start(self.interval, now=False)  # 这是一个定时执行某任务的模块啊

    def check_shutdown(self, spider):
        count = self.stats.get_value("mbs/new_record", 0)
        if count == self.count_cache:  # 检测到没有更新数据，则立即执行杀掉爬虫的指令
            self.crawler.engine.close_spider(spider, "shutdown by ShutDownNews extension")
        else:
            self.count_cache = count  # 有新数据，增更新数据到临时缓存

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
