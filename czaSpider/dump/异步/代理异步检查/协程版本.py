import aiohttp
import asyncio

sem = asyncio.Semaphore(10)


def raw_to_useful_async():
    loop = asyncio.get_event_loop()
    raw_proxies = ['60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797']
    tasks = [ping_async(proxy) for proxy in raw_proxies]
    loop.run_until_complete(asyncio.wait(tasks))
    for i in tasks:
        print(i)

def valid_useful_proxy_async(proxy):
    ret = yield ping_async(proxy)
    if ret:...
        # self.redis.hset(self.useful_proxy_queue, raw_proxy, 0)
        # self.redis.hdel(self.raw_proxy_queue, raw_proxy)
        # self.log.info('ProxyRefreshSchedule: %s validation pass' % raw_proxy)
    ret = yield ping_async(None)
    if ret:...
        # count += 1
        # if count >= FAIL_COUNT:
        #     self.redis.hdel(self.raw_proxy_queue, raw_proxy)
        # else:
        #     self.redis.hset(self.raw_proxy_queue, raw_proxy, count)
        # self.log.info('ProxyRefreshSchedule: %s validation fail' % raw_proxy)
    raise Exception("无法访问外网，验证代理程序终止")

async def ping_async(proxy):
    async with sem:
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            proxy = proxy and "{sch}://{proxy}".format(sch="http", proxy=proxy)
            try:
                async with session.get('http://httpbin.org/ip', proxy=proxy, timeout=1, allow_redirects=False) as response:
                    if response.status == 200 and 'origin' in await response.json():
                        print('验证成功', proxy)
                        return True
                    print('验证...', proxy, response.status)
                    return False
            except:
                print('超时了吧')
                return False



if __name__ == '__main__':
    raw_to_useful_async()
