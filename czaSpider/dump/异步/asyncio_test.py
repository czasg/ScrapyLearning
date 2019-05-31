"""
生产者消费者
对于生成器来说，你定义好了，但是没有启动的话，他是一个都不会执行的
在生成器中return，就会直接结束，你return什么都没用，只会跑出你的返回
"""
def example_first():
    def consumer():
        r = "Hello World!"  # 我虽然yield回去了，但是实际上并没有人来使用这个数据
        while True:
            n = yield r  # 启动后生成器会卡在这儿，等待后续的c.send继续启动
            if not n:
                print("会有人走到者来吗?")  # 如果在生成器里面return，会直接报错StopIteration吗
                return
            print("#####消费者#####: %s" % n)
            r = "200 ok"

    def producer(c):
        print("我居然是第一个打印的，太牛逼了吧")
        c.send(None)  # 第一步启动生成器这里一定要send一个None值吗
        n = 0
        while n < 5:
            n += 1
            print("#####生产者#####: %s" % n)
            r = c.send(n)
            print("#生产者接收参数#: %s" % r)
        c.close()

    c = consumer()  # 实例化一个生成器，其实生成里面什么都没开始跑！
    producer(c)  # 首先跑的第一句话居然还是生产者里面的！

# example_first()

import asyncio
"""
asyncio
@asyncio.coroutine会把一个生成器标记为协程类型，然后把这个协程扔到EvenLoop中执行
关键的是整个过程，是由一个单线程来实现的，当我们传入了两个
"""
@asyncio.coroutine
def hello():
    print("Hello World!")
    r = yield from asyncio.sleep(1)
    print("Hello World!")

def example_second():
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

example_second()
