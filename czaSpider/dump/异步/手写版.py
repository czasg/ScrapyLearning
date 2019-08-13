#coding:utf-8
from threading import Thread
from time import sleep

def async_decorator(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async_decorator
def A():
    sleep(4)
    print('heihei')

def B():
    print('HaHa')

A()
B()