from czaSpider import pipelines
from czaSpider import middlewares


from functools import reduce
def setting_plus(*settings):
    def add(setting1, setting2): # this is a func to fuse the dict, add all to the setting1
        new_setting = setting1.copy()  # 保留一份新的字典，以
        for s in setting2: # traverse the setting2 as s
            if s not in setting1: # if it is a key and not in setting1, go here
                new_setting[s] = setting2[s] # find different element from setting2, and add them to new_setting?
            elif isinstance(setting2[s], dict): # if the value is dict, recursive the func add
                new_setting[s] = add(setting1[s], setting2[s])
            elif setting2[s] == setting1[s]:
                pass
            else:
                raise ValueError("非字典类型的同名setting不能合并 %s" % str(s))
        return new_setting

    return reduce(add, settings)


def get_custom_settings(name, saveSource=False):
    if saveSource:
        return getattr(pipelines, "sourcePipeline_setting")
    return getattr(pipelines, name[name.rfind('-') + 1:] + "Pipeline_setting")


if __name__ == "__main__":
    a = get_custom_settings("cza-housePrice")
    print(type(a))
    print(a)

