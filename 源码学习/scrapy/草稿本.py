import pkg_resources


def run_entry_point(data):
    group = 'package?'
    for entrypoint in pkg_resources.iter_entry_points(group=group):
        print('entrypoint:', entrypoint)
        plugin = entrypoint.load()
        plugin(data)

run_entry_point(100)

"""
engine_started = object()               # 在引擎正式启动，也就是爬虫crawl里执行yield engine.start时发送此信号
engine_stopped = object()               # 引擎正式关闭，
spider_opened = object()
spider_idle = object()
spider_closed = object()
spider_error = object()
request_scheduled = object()            # 在执行一次调度的时候发送此信号
request_dropped = object()              # 在调度的时候，请求指纹过滤，要是被过滤掉了，则发送此信息
request_reached_downloader = object()
response_received = object()
response_downloaded = object()
item_scraped = object()
item_dropped = object()
item_error = object()
"""

"""
当你想要强制关闭爬虫的时候，可以主动捕获signal，来进行对应的处理。如：
    crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)  # 主要绑定spider_closed信号
    def spider_closed(self, spider):
        task = getattr(self, 'task', False)
        if task and task.active():
            task.cancel()

    # zty版本：from_crawler创建实例后，在init中绑定相关信号机制。
    def spider_opened(self, spider):
        self.task = task.LoopingCall(self.check_shutdown, spider)  # 一个定时执行任务的defer
        self.task.start(self.interval, now=False)
    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()

编写extensions拓展模块，需要实例化一个from_crawler进行初始化，init中可以绑定相关属性
你甚至可以主动触发引擎的关闭机制，如下：
self.crawler.engine.close_spider(spider, "shutdown by ShutDownNews extension")
"""