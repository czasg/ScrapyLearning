__FILE__ = "NOTE BOOK"

"""
通过在scrapy命令行中输入-s key=value，则可以在爬虫中使用self.crawler.settings.get("key")的方式获取

scrapy中response.request就是代表一个Request对象，且是上一级的请求对象。而response.request.callback则是指接受此response对象的函数
或者使用yield response.request.replace(url=new_page, dont_filter=True)，这种scrapy会默认附带我们需要的其他参数嘛
response.request.body.decode()这个好像是代表访问的url
yield Request(url).replace(meta={"url":url})可以使用这种方式传递meta，很强页很骚

request payload请求方式，传送数据是json，需要使用Request(self.url, body=json.dumps(data), method="POST", headers=headers)，头为"application/json;charset=UTF-8"

handle_httpstatus_list = [521, 404] 这是一个scrapy自带的中间件模块里的属性，允许该类型的状态码通过而不是直接过滤

from urllib.parse import *
unescape 对转义字符做处理
urlparse
urlunparse
parse_qs 获取url中的参数，返回字典
parse_qsl 获取url中的参数，返回列表
quote 能接收两个参数，第一个是url，第二是安全字符，即加密过程该类字符不变，默认为"/"
quote_plus 该函数能将空格转变为+号，且安全字符默认为空
quote_from_bytes 接收的是字节，而非字符串
unquote
unquote_plus
unquote_to_bytes
urlencode 拼接元素使称为url后缀参数

对于多线程会重复解析的问题，可以通过手动分配线程任务来避免任务被重复解析。以id最后一位计算，除以线程数就可以分配线程任务了
"""