"""
Scrapy extension for collecting scraping stats
"""
import pprint
import logging

logger = logging.getLogger(__name__)


class StatsCollector(object): # spider.crawler.stats.inc_value("scanned/urls", count=urls) / spider.crawler.stats.inc_value("scanned/new_urls", count=new_urls)

    def __init__(self, crawler): # 一个统计源码
        self._dump = crawler.settings.getbool('STATS_DUMP')  # STATS_DUMP = True
        self._stats = {}

    def get_value(self, key, default=None, spider=None):
        return self._stats.get(key, default)

    def get_stats(self, spider=None):
        return self._stats

    def set_value(self, key, value, spider=None):
        self._stats[key] = value  # 自定义设置初始值

    def set_stats(self, stats, spider=None):  # 自定义设置咯，估计是一个字典?
        self._stats = stats

    def inc_value(self, key, count=1, start=0, spider=None):  # 用的是这个，对已有值进行累加把
        d = self._stats
        d[key] = d.setdefault(key, start) + count  # 又get新知识了，字典setdefault返回默认值，我的天呢

    def max_value(self, key, value, spider=None):
        self._stats[key] = max(self._stats.setdefault(key, value), value)  # 和已有值相比，保存最大的值

    def min_value(self, key, value, spider=None):
        self._stats[key] = min(self._stats.setdefault(key, value), value)  # 和已有值相比，保存最小的值

    def clear_stats(self, spider=None):
        self._stats.clear()  # 字典执行clear，直接再见

    def open_spider(self, spider):
        pass

    def close_spider(self, spider, reason):
        if self._dump:
            logger.info("Dumping Scrapy stats:\n" + pprint.pformat(self._stats),
                        extra={'spider': spider})
        self._persist_stats(self._stats, spider)

    def _persist_stats(self, stats, spider):
        pass


class MemoryStatsCollector(StatsCollector):

    def __init__(self, crawler):
        super(MemoryStatsCollector, self).__init__(crawler)
        self.spider_stats = {}

    def _persist_stats(self, stats, spider):
        self.spider_stats[spider.name] = stats  # 把最终统计结果传到spider_stats里面嘛


class DummyStatsCollector(StatsCollector):

    def get_value(self, key, default=None, spider=None):
        return default

    def set_value(self, key, value, spider=None):
        pass

    def set_stats(self, stats, spider=None):
        pass

    def inc_value(self, key, count=1, start=0, spider=None):
        pass

    def max_value(self, key, value, spider=None):
        pass

    def min_value(self, key, value, spider=None):
        pass


