formData = """

access_token: ""
local_province_id: "42"
local_type_id: 1
page: 1
school_id: "42"
signsafe: "905c301c8585745cff80dbb7e72c53d4"
size: 20
uri: "apidata/api/gk/score/special"
year: 2018

"""


def transform(data):
    for i in data.strip().split('\n'):
        print(': '.join(["'%s'" % j.strip() for j in i.split(":", 1)]) + ',')


transform(formData)

""" post请求参数手动转化的方法1 """
from urllib.parse import urlencode

data = {
    'newmap': '1',
    'reqflag': 'pcmap',
    'biz': '1',
    'from': 'webmap',
    'da_par': 'direct',
    'pcevaname': 'pc4.1',
    'qt': 's',
    'da_src': 'searchBox.button',
    'wd': '武汉 联投梧桐郡悦园',
    'c': '218',
    'src': '0',
    'wd2': '',
    'pn': '0',
    'sug': '0',
    'l': '12',
    'b': '(12699769.29,3538757.28;12740217.29,3578757.28)',
    'from': 'webmap',
    'biz_forward': '{"scaler":1,"styles":"pl"}',
    'sug_forward': '',
    'auth': 'df15XFWzeDvfPVX34=AY0GXfONFNQDfNuxHLVzHzRxxtAmk5zC88yy1uVt1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtPWv3GuxtVwi04960vyACFIMOSU7ucEWe1GD8zv7u@ZPuVteuztexZFTHrwzBvprGnrFHQUcJQJWcNEhl44yHxvaaZyB',
    'device_ratio': '1',
    'tn': 'B_NORMAL_MAP',
    'nn': '0',
    'u_loc': '12738227,3543955',
    'ie': 'utf-8',
    't': '1560252819337',
}
# print(urlencode(data))

# import requests
# requests.get('', params={})