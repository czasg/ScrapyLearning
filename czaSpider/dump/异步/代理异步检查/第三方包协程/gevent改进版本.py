import requests
import gevent
from gevent import monkey
from gevent.pool import Pool

# 把当前的IO操作，打上标记，以便于gevent能检测出来实现异步(否则还是串行）
monkey.patch_all()


def task(url):
    response = requests.get(url)
    print(response.status_code)


# 控制最多一次向远程提交多少个请求，None代表不限制
pool = Pool(5)
gevent.joinall([
    pool.spawn(task, url='https://www.baidu.com'),
    pool.spawn(task, url='http://www.sina.com.cn'),
    pool.spawn(task, url='https://news.baidu.com'),
])

# gevent + reqeust + Pool（控制每次请求数量）