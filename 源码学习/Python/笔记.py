__file__ = '笔记'

"""
优化内存。使用生成器，使用__slots__


"""


if __name__ == '__main__':
    a = [str(i)+j for i in range(5)
                  for j in 'abcde']
    print(a)