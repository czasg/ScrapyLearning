class Test:
    def __init__(self):
        self.__dict__ = {}

    def __setattr__(self, key, value):
        if key.startswith('__'):
            return
        self.__dict__[key] = self.__dict__.get(key, '') + value

    def __getattr__(self, item):
        return self.__dict__.get(item, '')

if __name__ == '__main__':
    a = Test()
    a.cza = '123'
    print(a.cza)
    a.cza = '456'
    print(a.cza)
