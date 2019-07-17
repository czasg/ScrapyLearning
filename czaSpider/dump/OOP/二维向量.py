from math import hypot


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%s, %s)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x or self.y) # bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


if __name__ == '__main__':
    test = Vector(1, 2)
    # print(test)
    print(bool(test))


"""
__repr__: 将对象用字符串的形式表达出来，还有一个__str__函数，二者区别是后者会在str()函数被使用或者print函数被使用时打印
如果只能实现这里面的一个，推荐__repr__，因为当一个对象没有__str__函数的时候，解释器会调用__repr__进行替代

"""