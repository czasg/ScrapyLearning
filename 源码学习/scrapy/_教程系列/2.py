__title__ = '实现异步下载'


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
    start_urls = ['http://www.czasg.xyz', 'http://www.czasg.xyz',
                  'http://www.czasg.xyz', 'http://www.czasg.xyz']

    def start_requests(self):
        yield from (Request(url, self.parse) for url in self.start_urls)

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':
    spider = MySpider()

    import aiohttp
    import asyncio


    async def _download(request):  # scrapy是基于Twisted实现的异步下载，此处aiohttp也是凑凑
        async with aiohttp.ClientSession() as session:
            async with session.get(request.url) as response:
                byte_content = await response.content.read()  # 用aiohttp模拟异步下载, 获取DOM
                response = Response(byte_content, request)    # 构建Response对象
                request.callback(response)  # 执行回调


    loop = asyncio.get_event_loop()
    tasks = [_download(request) for request in spider.start_requests()]
    loop.run_until_complete(asyncio.wait(tasks))

"""手写(si)Scrapy(二)
请勿随意转载~Thank You~
最近看Scrapy源码(看不懂==脑壳疼)，想尝试一下能否模仿出此框架的大致流程。顺便记录下实现过程。
并非是要重复造轮子，只是想试试而已~
计划实现步骤：
1、基本的Request/Response (完成)
2、实现异步下载 (当前进度)
3、加入队列Queue，为实现调度器做准备
4、加入引擎管理
5、加入调度器管理
6、加入下载器管理
7、加入下载器中间件管理
8、加入爬虫进程管理
9、加入信号机制管理
"""

"""
在上一节中，我们通过
用过Scrapy的朋友，应该对以下代码有点熟悉
class MySpider(spider.Spider):
    name = 'spider_name'
    start_urls = ['www.czasg.xyz']

    def parse(response):
        print(response.url)

以上代码是Scrapy框架中的爬虫文件，在我个人接触的爬虫中，使用较多的还有pipeline管道、middleware中间件。而调度器和引擎基本没怎么接触。

现在先模拟Request 和 Response 把        


"""
