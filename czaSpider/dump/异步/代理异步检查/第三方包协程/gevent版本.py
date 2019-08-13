import requests
import gevent
from gevent import monkey as curious_george

#把当前的IO操作，打上标记，以便于gevent能检测出来实现异步(否则还是串行）
curious_george.patch_all(thread=False, select=False)


def task(url):
    response = requests.get(url)
    print(response.status_code)

gevent.joinall([
    gevent.spawn(task,url='https://www.baidu.com'),
    gevent.spawn(task,url='http://www.sina.com.cn'),
    gevent.spawn(task,url='https://news.baidu.com'),
])
