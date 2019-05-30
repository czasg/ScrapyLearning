def cover_dict(default, override):
    new_dict = default.copy()
    for key, value in override.items():
        if key in default:
            if isinstance(value, dict):
                new_dict[key] = cover_dict(default[key], value)
            else:
                new_dict[key] = value
    return new_dict


def merge_dict(dictionary1, dictionary2):
    new_dict = dictionary1.copy()
    if dictionary1 and dictionary2:
        for key, value in dictionary2.items():
            if key not in dictionary1:
                new_dict[key] = value
            elif isinstance(value, dict):
                new_dict[key] = merge_dict(dictionary1[key], dictionary2[key])
    return new_dict


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


class Record(dict):
    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
