# import requests
# from concurrent.futures import ThreadPoolExecutor
#
# pool = ThreadPoolExecutor(13)
#
# def request(proxy):
#     proxies = proxy and {sch: "{sch}://{proxy}".format(sch=sch, proxy=proxy) for sch in ["http", "https"]}
#     try:
#         r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
#         if r.status_code == 200 and r.json().get("origin"):
#             return True
#         return False
#     except:
#         return False
#
# def read_data(future,*args,**kwargs):
#     response = future.result()
#     print(response)
#
# def valid_useful_proxy_thread(proxy):
#     print('11')
#     return pool.submit(request, proxy)
#
# def main():
#     raw_proxies = ['60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#                    '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797']
#     count = 0
#     for proxy in raw_proxies:
#         count += 1
#         # done = pool.submit(request, proxy)
#         # done.add_done_callback(read_data)
#         # done = valid_useful_proxy_thread(proxy)
#         # done.add_done_callback(read_data)
#         def _callback(future, count=count):
#             r = future.result()
#             if r:
#                 print(count, r)
#             else:
#                 print(count, r)
#
#         done = pool.submit(request, proxy)
#         done.add_done_callback(_callback)
#
#
#
#     # done = pool.submit(request)
#     # done.add_done_callback(read_data)
#
# if __name__ == '__main__':
#     import time
#     now = time.time()
#     main()
#     pool.shutdown(wait=True)
#     # print('using:', int(time.time()-now))
#
#     # raw_proxies = ['60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#     #                '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#     #                '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
#     #                '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797']
#     # for i in raw_proxies:
#     #     print(request(i))
#     print('using:', int(time.time() - now))

# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import time

from config.setting import proxy_getter_functions
# from tools.spiders import GetFreeProxy
from tools.util_function import verify_proxy_format, valid_useful_proxy, get_redis

FAIL_COUNT = 1  # 校验失败次数， 超过次数删除代理


class ProxyManager:
    def __init__(self):
        self.raw_proxy_queue = 'proxy:raw'
        self.log = logging.getLogger(self.__class__.__name__)
        self.useful_proxy_queue = 'proxy:useful'
        self.redis = get_redis()

    def refresh(self):
        """
        爬取新的代理放进数据库(不验证)
        """
        for proxyGetter in proxy_getter_functions:
            self.log.info("{getter} started".format(getter=proxyGetter))
            proxy_set = set()

            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                proxy_iter = [_ for _ in getattr(GetFreeProxy, proxyGetter.strip())()]

            except:
                self.log.error("{func}: fetch proxy fail".format(func=proxyGetter))
                continue

            for proxy in proxy_iter:
                proxy = proxy.strip()
                if proxy and verify_proxy_format(proxy):
                    self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                    proxy_set.add(proxy)
                else:
                    self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))

            # 存储
            for proxy in proxy_set:
                if self.redis.hexists(self.useful_proxy_queue, proxy):
                    continue
                self.redis.hset(self.raw_proxy_queue, proxy, 1)
            self.log.info("{getter} ended".format(getter=proxyGetter))

    def get_all(self):
        """
        get all proxy from pool as list
        """
        item_dict = self.redis.hgetall(self.useful_proxy_queue)
        return list(item_dict.keys()) if item_dict else list()

    def raw_to_useful(self):
        """
        验证raw_proxy_queue中的代理, 将可用的代理放入useful_proxy_queue
        随机取出一个raw验证通过后丢入useful
        """
        self.log.info('ProxyRefreshSchedule: %s start validProxy' % time.ctime())
        raw_proxies = self.redis.hgetall(self.raw_proxy_queue)
        for raw_proxy, count in raw_proxies.items():
            count = count and int(count) or 0
            if valid_useful_proxy(raw_proxy):
                self.redis.hset(self.useful_proxy_queue, raw_proxy, 0)
                self.redis.hdel(self.raw_proxy_queue, raw_proxy)
                self.log.info('ProxyRefreshSchedule: %s validation pass' % raw_proxy)
            else:
                count += 1
                if count >= FAIL_COUNT:
                    self.redis.hdel(self.raw_proxy_queue, raw_proxy)
                else:
                    self.redis.hset(self.raw_proxy_queue, raw_proxy, count)
                self.log.info('ProxyRefreshSchedule: %s validation fail' % raw_proxy)
        self.log.info('ProxyRefreshSchedule: %s validProxy complete' % time.ctime())

    def drop_useless(self):
        # 验证成功一次减1直到0验证失败一次加1如果超限则删除
        proxies = self.redis.hgetall(self.useful_proxy_queue)
        for proxy, count in proxies.items():
            count = count and int(count) or 0  # count表示验证失败的次数
            if valid_useful_proxy(proxy):  # 验证通过计数器减1
                if count > 0:
                    self.redis.hset(self.useful_proxy_queue, proxy, count - 1)
                self.log.info('ProxyCheck: {} validation pass'.format(proxy))
            else:
                self.log.info('ProxyCheck: {} validation fail'.format(proxy))
                count += 1
                if count >= FAIL_COUNT:
                    self.log.info('ProxyCheck: {} fail too many, delete!'.format(proxy))
                    self.redis.hdel(self.useful_proxy_queue, proxy)
                else:
                    self.redis.hset(self.useful_proxy_queue, proxy, count)

    def raw_to_useful_multi_thread(self, thread=12):
        from concurrent.futures import ThreadPoolExecutor

        pool = ThreadPoolExecutor(thread)
        raw_proxies = self.redis.hgetall(self.raw_proxy_queue)
        self.log.info('ProxyRefreshSchedule: %s start validProxy' % time.ctime())

        for raw_proxy, count in raw_proxies.items():
            count = count and int(count) or 0

            def _callback(future, count=count):
                if future.result():
                    self.redis.hset(self.useful_proxy_queue, raw_proxy, 0)
                    self.redis.hdel(self.raw_proxy_queue, raw_proxy)
                    self.log.info('ProxyRefreshSchedule: %s validation pass' % raw_proxy)
                else:
                    count += 1
                    if count >= FAIL_COUNT:
                        self.redis.hdel(self.raw_proxy_queue, raw_proxy)
                    else:
                        self.redis.hset(self.raw_proxy_queue, raw_proxy, count)
                    self.log.info('ProxyRefreshSchedule: %s validation fail' % raw_proxy)

            done = pool.submit(valid_useful_proxy, raw_proxy)
            done.add_done_callback(_callback)
