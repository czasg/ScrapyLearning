import re

class FakeSREMatch:
    def __init__(self, pattern, flags):
        self.count = re.compile(pattern, flags).groups

    def group(self, index):
        assert isinstance(index, int), "rea的group方法目前只支持一个int参数"
        if index in range(0, self.count + 1):
            return None
        raise IndexError("no such group")

    def groups(self):
        return (None,) * self.count

    def groupdict(self):
        return {}


def search(pattern, string, flags=0):
    """
    功能同re.search 当未匹配到时，group()和groups()不会报错
    """
    return string is not None and re.search(pattern, string, flags) or FakeSREMatch(pattern, flags)


if __name__ == '__main__':
    print(search('(?:)(\d+)(?=)', '').groups())