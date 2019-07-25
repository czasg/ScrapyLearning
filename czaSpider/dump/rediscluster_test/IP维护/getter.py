from dump.rediscluster_test.IP维护.fff import RedisClient
from dump.rediscluster_test.IP维护.spider import Crawler


class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= 1000:
            return True
        else:
            return False

    def run(self):
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                cb = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(cb)
                for proxy in proxies:
                    print(proxy)
                    # self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
    pass
