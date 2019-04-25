def strJoin(string, sepJ="", sep=None, maxNum=-1):
    """
    切割string，然后join
    :param string: 输入字符串
    :param sepJ: join切割后的字符串，所使用的符号，默认为空
    :param sep: 按sep规则进行切割
    :param maxNum: 最大切割次数，默认为-1，即不限
    :return: 切割后合并字符串
    """
    return sepJ.join(string.split(sep, maxsplit=maxNum))


def arrayJoin(array, func=None, sepJ="", strict=False, **kwargs):
    """
    对list或tuple或str进行join合并
    :param array: 输入
    :param func: 针对array中每一组的操作，默认为strJoin
    :param sepJ: 合并使用的符号
    :param strict: 是否对每一个内容进行处理
    :param kwargs: 当输入为str时，同样进行切割，可以指定sep和maxNum来辅助切割
    :return:
    """
    if isinstance(array, str):
        sep = kwargs.get("sep", "")
        maxNum = kwargs.get("maxNum", -1)
        array = array.split(sep, maxsplit=maxNum)
    function = func or strJoin
    array = [each for each in array if each]
    return sepJ.join(map(function, array)) if strict else sepJ.join(array)


def array_strip(array):
    """
    对array中每一个元素进行strip处理
    :param array:
    :return:
    """
    if isinstance(array, str):
        array = [array]
    return [string.strip() for string in array]


def dict_strip(_dict, key=True, value=False):
    """
    对dict中的相关进行去空格操作
    :param _dict: 输入字典
    :param key: 默认仅对key进行去空格处理
    :param value: 增加对value的处理
    :return:
    """
    if key and value:
        _dict = {strJoin(key): strJoin(value) for key, value in _dict.items()}
    elif key:
        _dict = {strJoin(key): value for key, value in _dict.items()}
    return _dict


if __name__ == "__main__":
    # print(strJoin('cza is sg'))
    # print(arrayJoin(['cz  a', 'shs  hs', '6  66']))
    # print(arrayJoin(['cz  a', 'shs  hs', '6  66'], strict=True))
    print(dict_strip({"1 2 3": "cz ai ss g"}, value=True))
