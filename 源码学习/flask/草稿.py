class TestDes:
    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter
    def __get__(self, instance, owner): return self.__name__
    def __set__(self, instance, value): self.__name__ = value

class TestMain:
    des = TestDes('Test')

if __name__ == '__main__':
    t = TestMain()
    # print(t.des)
    # print(TestMain.des)  # 不需要实例化也能够直接拿到属性嘛，可以啊
