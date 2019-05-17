def cover_dict(default, override):
    new_dict = default.copy()
    for key,value in override.items():
        if key in default:
            if isinstance(value, dict):
                new_dict[key] = cover_dict(default[key], value)
            else:
                new_dict[key] = value
    return new_dict

def merge_dict(dictionary1, dictionary2):
    new_dict = dictionary1.copy()
    if dictionary1 and dictionary2:
        for key,value in dictionary2.items():
            if key not in dictionary1:
                new_dict[key] = value
            elif isinstance(value, dict):
                new_dict[key] = merge_dict(dictionary1[key], dictionary2[key])
    return new_dict




# a={"key":"key",}
# b={"new":"new"}
# print(merge_dict(a,b))


# def func(**kwargs):
#     print(kwargs)
#
# func(test='test', haha="haha")