# from czaSpider.czaBaseSpider import IOCO
# from czaSpider.czaTools import *
#
# from scrapy import Selector
#
# from minitools.scrapy import xt
# from minitools import merge_dict
#
#
# class MySpider(IOCO):
#     name = "hello-test2"
#
#     url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=python%E5%A6%82%E4%BD%95%E5%88%A4%E6%96%AD%20%20%E6%98%AF%E5%90%A6%E4%B8%BA%E5%87%BD%E6%95%B0&oq=python%25E5%25A6%2582%25E4%25BD%2595%25E5%2588%25A4%25E6%2596%25AD%2520%25E5%2587%25BD%25E6%2595%25B0&rsv_pq=a2314b1d0013524a&rsv_t=b05fHd08nIAqasC1wrNhl8HxWTCLv%2B7OPJ9urcbx6KdFpPSpWzlTmlNBUZI&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=1451&rsv_sug3=22&rsv_sug1=9&rsv_sug7=100&rsv_sug2=0&rsv_sug4=2790"
#
#     def parse(self, response):
#         # print(len(from_xpath(response, '//*[@class="result c-container "]', type=1)))
#         # print(from_xpath(response, '//a/@href', typing.urljoin))
#         # print(from_xpath(response, '//*[@id="content_left"]', xt.analysis_article))
#
#         # for data in from_xpath(response, [
#         #     '//*[@class="result c-container "]',
#         #     # ['./h3//text()', 2, dict(sep='|'), lambda x: x == 'python|之类中|如何判断是函数|还是方法 - Xcsg - 博客园'],
#         #     ['./h3/a/@href', 3],
#         # ]):
#         #     print(data)
#         pass
#
# if __name__ == '__main__':
#     MySpider.cza_run_spider()


import requests
from parsel import Selector
from minitools.scrapy import from_xpath, xt

url = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=python%20%20setuptools%20%20install_requires%E5%A6%82%E4%BD%95%E5%86%99&oq=python%2520setuptools%2520extras_require%2520%25E5%25A6%2582%25E4%25BD%2595%25E5%2586%2599&rsv_pq=e52274de0013037d&rsv_t=c82cqGQWBYJZ4EI7tl9xDctZ34KZsdU1T6QxrNIoOvCkkiGdXFOGILpzOGU&rqlang=cn&rsv_enter=0&rsv_dl=tb&inputT=1464&rsv_sug3=32&rsv_n=2&rsv_sug4=1671"
text = requests.get(url).text


class _Selector(Selector):
    __slots__ = ['text', 'namespaces', 'type', '_expr', 'root',
                 '_parser', '_csstranslator', '_tostring_method', 'base_url']

    def __init__(self, text=None, type=None, namespaces=None, root=None,
                 base_url=None, _expr=None):
        self.base_url = base_url
        super(_Selector, self).__init__(text, type, namespaces, root, base_url, _expr)

    def urljoin(self, url):
        from urllib.parse import urljoin
        return urljoin(self.base_url, url)


response = _Selector(text=text, base_url=url)
# print(from_xpath(response, '//*[@class="result c-container "]'))
for title, url in from_xpath(response, [
    '//*[@class="result c-container "]',
    ['./h3//text()', xt.string_join],
    ['./h3/a/@href', xt.urljoin]
]):
    print(title, url)
