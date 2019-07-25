import aiohttp
import asyncio
import time

from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from dump.rediscluster_test.IP维护.fff import RedisClient
from aiohttp import ClientError



class Tester:
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                async with session.get('', proxy=real_proxy, timeout=1, allow_redirects=False) as response:
                    if response.status in ['200']:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
            except:
                self.redis.decrease(proxy)

    def run(self):
        try:
            count  = self.redis.count()
            for i in range(0, count):
                start = i
                stop = i + 1
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
        except:
            pass


