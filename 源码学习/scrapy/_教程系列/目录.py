__file__ = '目录'


"""
基本的Request或Response对象管理


实现异步下载


加入队列Queue


加入引擎管理


加入调度器管理


加入下载器管理


加入中间件管理


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
