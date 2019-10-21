def test():
    yield 5

    yield 6


if __name__ == '__main__':
    # for i in test():
#     #     print(i)
    print(test())
