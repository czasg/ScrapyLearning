from __future__ import absolute_import  # 绝对导入???
from importlib import import_module
from pkgutil import iter_modules
import inspect
import signal
from pydispatch import dispatcher
import sys
import weakref; weakDict = weakref.WeakKeyDictionary()  # 弱引用
def property_test():
    class test:
        def __init__(self, x):
            self._x = x
        def getx(self):
            return self.x
        x = property(lambda self: self._x, doc='test')
    a = test(1)
    print(a.x)  # t这种写法还有点骚，直接用@property还好看一点
def signal_test(signal1, signal2, test2=True):
    if test2:
        dispatcher.connect(vars_dir_deff_test, signal=signal1)
        dispatcher.connect(vars_dir_deff_test, signal=signal2)
    else:
        class test:
            def __init__(self, x):
                self._x = x
                self.flag = False
            def start(self):
                signal.signal(signal.SIGTERM, self._term_handler)
                signal.signal(signal.SIGINT, self._term_handler)
                count = 0
                while not self.flag:
                    import time
                    count += 1
                    print(count)
                    time.sleep(1)
            def _term_handler(self, signal_num, frame):
                print('get termnum is : ', signal_num, frame)
                self.flag = True
        a = test(2)
        a.start()
def walk_module_test():
    path = 'scrapy.commands'
    mod = import_module(path)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            if subpath == 'crawl':
                fullpath = path + '.' + subpath
                submod = import_module(fullpath)
                for ke, obj in vars(submod).items():
                    if inspect.isclass(obj):
                        print(ke, obj)
                        print(obj.__module__ == submod.__name__, obj.__module__, mod.__name__)
def vars_dir_deff_test():
    class test:
        def __init__(self):
            self.x = None
            self.y = None
        def test1(self):
            pass
    print(vars(test))
    print(dir(test))
    dir()
    # dir只打印属性（属性, 属性......），已列表list形式返回
    # 而vars()
    # 则打印属性与属性的值（属性：属性值......），以字典dict形式返回
if __name__ == '__main__':
    from pydispatch import dispatcher
    from pydispatch.dispatcher import Any, Anonymous, liveReceivers, \
        getAllReceivers, disconnect

    test_signal = object()
    def handle_event(sender):
        """Simple event handler"""
        print('Signal was sent by', sender)
    dispatcher.connect(handle_event, signal=test_signal, sender=dispatcher.Any)  # 链接操作，链接函数handle_event，信号为SIGNAL，是一个不错的回调模块
    first_sender = object()
    second_sender = 'cza'
    for receiver in liveReceivers(getAllReceivers(first_sender, signal)):
        print(receiver)

    dispatcher.send(signal=test_signal, sender=first_sender)
    dispatcher.send(signal=test_signal, sender=second_sender)

    pass