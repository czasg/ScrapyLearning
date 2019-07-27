# -*- utf-8 -*-
import aiohttp
import asyncio

from redis_man import Redis
from setting import Setting as config

sem = asyncio.Semaphore(config.async_sem)


class Checker:
    def __init__(self):
        self.redis = Redis.from_setting(config)
        self.setting = config

    async def check(self, proxy, flag=0):
        async with sem:  # 设定异步并发大小
            conn = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=conn) as session:
                try:
                    http_proxy = 'http://' + proxy.decode()
                    async with session.get(self.setting.proxy_test_url,
                                           timeout=1,
                                           allow_redirects=False,
                                           proxy=http_proxy) as response:
                        if response.status in self.setting.allow_status:
                            flag = 1
                except:
                    pass
                if not flag:
                    self.redis.decrease(proxy)

    def start(self, start=0):
        count = self.redis.count()
        sep = min(count // 4, self.setting.redis_batch_sep)
        loop = asyncio.get_event_loop()
        for i in range(0, count, sep):
            if i == 0:
                continue
            stop = i
            proxy_pool = self.redis.batch(start, stop)
            tasks = [self.check(proxy) for proxy in proxy_pool]
            loop.run_until_complete(asyncio.wait(tasks))
            start = stop
        loop.close()


if __name__ == '__main__':
    checker = Checker()
    checker.start()
