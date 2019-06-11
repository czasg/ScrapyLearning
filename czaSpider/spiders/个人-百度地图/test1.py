from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

""" 百度地图为了更加精确，应该使用原来的地址进行查找
对于手动构建的请求，在scrapy中可以使用FormRequest进行请求，但是requests中怎么做呢？

from urllib.parse import urlencode

requests.get(url, param)
"""
class MySpider(IOCO):
    name = "baidu-map"

    page = 1
    url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=shareurl&wd=%E6%AD%A6%E6%B1%89%E7%BB%BF%E5%9C%B0%E5%9F%8E&c=218&src=0&pn=0&sug=0&l=17&b=(12697083.314516129,3525274.1388172046;12698714.905268816,3526646.4911827953)&from=webmap&biz_forward=%7B%22scaler%22:1,%22styles%22:%22pl%22%7D&device_ratio=1&auth=xM6Z9aSCFFKJ3SP9gdIFMHyR4bSZOHCQuxHLVzEVBNBt0A%3DH73uzCywi04vy77u1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtPWv3GuxtVwi04960vyACFIMOSU7ucEWe1GD8zv7u%40ZPuVteuVtegvcguxHLVzEVBNBtquTTGdFrZZWuV&tn=B_NORMAL_MAP&nn=0&u_loc=12735320,3550913&ie=utf-8&t=1560240376314'

    formData = {
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

    def start_requests(self):
        key = "北京  燕郊-京平高速木燕路(北务出口)东500米"
        url = "https://map.baidu.com/"
        formData = self.formData
        formData['wd'] = key
        yield FormRequest(url, method='GET', formdata=formData)

    def parse(self, response):
        print(response.url)
        aaa = json.loads(response.text)
        print(aaa['content'])
        # print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
