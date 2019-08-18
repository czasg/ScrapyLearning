class TestDes:
    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter
    def __get__(self, instance, owner): return self.__name__
    def __set__(self, instance, value): self.__name__ = value

class TestMain:
    des = TestDes('Test')

    @classmethod
    def fromkeys(cls, keys, value=None):
        from itertools import repeat
        instance = super(cls, cls).__new__(cls)  # 这种写法还是第一次见
        instance.__init__(zip(keys, repeat(value)))
        return instance


class locked_cached_property(object):
    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, None)
        if value is None:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
@locked_cached_property
def locked_cached_property_test():
    print('hello')

if __name__ == '__main__':
    # t = TestMain()
    # print(t.des)
    # print(TestMain.des)  # 不需要实例化也能够直接拿到属性嘛，可以啊

    a = locked_cached_property_test
    a.func()  # 这玩意会被当成一个属性存储着吗，当你调用的时候才会执行，，这
