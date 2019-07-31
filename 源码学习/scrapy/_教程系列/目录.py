__file__ = '目录'


"""
1基本的Request或Response对象管理


2实现异步下载


3加入队列Queue


4加入引擎管理


5加入调度器管理


6加入下载器管理  ## 这个没下好，下载器比这个难多了


7加入下载器中间件管理  ## 这个更不谈，


加入爬虫进程管理


加入信号机制管理

"""

if __name__ == '__main__':
    from treq import get as getPage
    from twisted.internet import reactor

    from treq.response import _Response

    def done(response):
        # print(response, dir(response))
        d = response.content()
        def test(response):
            print(response)
        d.addBoth(test)
        return d

    d = getPage("http://www.baidu.com").addCallback(done)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
