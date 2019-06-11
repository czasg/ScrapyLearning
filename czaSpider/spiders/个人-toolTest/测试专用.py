from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    page = 1
    url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=shareurl&wd=%E6%AD%A6%E6%B1%89%E7%BB%BF%E5%9C%B0%E5%9F%8E&c=218&src=0&pn=0&sug=0&l=17&b=(12697083.314516129,3525274.1388172046;12698714.905268816,3526646.4911827953)&from=webmap&biz_forward=%7B%22scaler%22:1,%22styles%22:%22pl%22%7D&device_ratio=1&auth=xM6Z9aSCFFKJ3SP9gdIFMHyR4bSZOHCQuxHLVzEVBNBt0A%3DH73uzCywi04vy77u1GgvPUDZYOYIZuVt1cv3uVtGccZcuVtPWv3GuxtVwi04960vyACFIMOSU7ucEWe1GD8zv7u%40ZPuVteuVtegvcguxHLVzEVBNBtquTTGdFrZZWuV&tn=B_NORMAL_MAP&nn=0&u_loc=12735320,3550913&ie=utf-8&t=1560240376314'


    # def start_requests(self):
    #     yield FormRequest(self.url, formdata=self.formData, headers=self.headers)

    def parse(self, response):
        print(response.url)
        aaa = json.loads(response.text)
        print(aaa['content'])


if __name__ == "__main__":
    MySpider.cza_run_spider()
