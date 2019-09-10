def merge(defaults, override):
    res = dict()
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                res[k] = merge(v, override[k])
            else:
                res[k] = override[k]
        else:
            res[k] = v
    return res


def toDict(di):
    res = Dict()
    for k, v in di.items():
        res[k] = toDict(v) if isinstance(v, dict) else v
    return res


class Dict(dict):
    def __init__(self, name=(), value=(), **kwargs):
        super(Dict, self).__init__(**kwargs)
        for k, v in zip(name, value):
            self[k] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            raise AttributeError('Dict object has not attributes: %s' % key)


from project_config import config_default
from project_config import config_override

configs = toDict(merge(config_default.configs, config_override.configs))
