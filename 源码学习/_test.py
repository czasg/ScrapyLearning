from importlib import import_module
from pkgutil import iter_modules
import inspect
import sys


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


if __name__ == '__main__':
    class test:
        def __init__(self, x):
            self._x = x

        def __del__(self):
            return "{}.....{}".format(self._x, id(self))

        def __str__(self):
            return "{}.....{}".format(self._x, id(self))

        __repr__ = __str__

    a1 = test(1)
    a2 = test(2)
    di = dict()
    di[a1] = 'xxx'
    di[a2] = 'yyy'
    print(di)
    del a1  # 就算我删除了对象，在字典中还是有引用的，删除之后对a1就不可控了，但是他会一直在dict里面吗
    del a2
    print(di)
    del di
    print(sys.getrefcount(test))
    # di.pop(a1)
    # print(di)  # 也没有办法取出来，这个废了