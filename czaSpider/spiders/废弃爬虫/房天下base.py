from scrapyProj.creditBaseSpider import LLBaseSpider
from scrapyProj.tools import *


def get_formData(key):
    formData = {
        "newmap": "1",
        "reqflag": "pcmap",
        "biz": "1",
        "from": "webmap",
        "da_par": "direct",
        "pcevaname": "pc4.1",
        "qt": "s",
        "da_src": "searchBox.button",
        "wd": key,
        "c": "300",
        "src": "0",
        "wd2": "",
        "pn": "0",
        "sug": "0",
        "l": "19",
        "b": "(13279221.885,2988709.99;13280181.885,2989194.99)",
        "biz_forward": '{"scaler":1,"styles":"pl"}',
        "sug_forward": "",
        "auth": "gzbDy@JSWvzNyFy4QVwRJ4weTE=HF=JEuxHLVBVxBxTtykiOxAXXw1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtPWv3GuxtVwi04960vyACFIMOSU7ulEeLZNz1VD=CUbB1A8zv7u@ZPuVteuxtf0wd0vyIM7C7yCySuvzXX3hJrZZWuV",
        "device_ratio": "1",
        "tn": "B_NORMAL_MAP",
        "nn": "0",
        "u_loc": "12735320,3550913",
        "ie": "utf-8",
        "t": "1560301332496",
    }
    return formData


def good_content(s):
    if "访问验证" in s:
        return False
    return True


class FangTianXiaBase(LLBaseSpider):
    name = "FangTianXiaBase"
    baidu = 'https://map.baidu.com/'
    custom_settings = csp.setting_plus(csp.ll_default_settings,
                                       {"URLLENGTH_LIMIT": 20000, "DOWNLOAD_DELAY": 1,
                                        "allowed_content": good_content})

    @classmethod
    def process_baidu(cls, response):
        try:
            source_code = json.loads(response.text)['content']
            baidu_address = source_code[0]['addr']
        except:
            source_code = json.loads(response.text)
            baidu_address = None
        yield cls.download_item(url=response.meta['url'],
                                html=[{"name": '房天下源码', "request": response.meta['source']},
                                      {"name": '百度源码', "request": json.dumps(source_code, ensure_ascii=False)}],
                                city_name=response.meta["city_name"],
                                m5=response.meta["m5"],
                                unique_key='m5',
                                baidu_address=baidu_address)
