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

在命令行中定义log级别与指定日志文件，使用scrapy crawl spider -s LOG_FILE=file.log --loglevel=INFO 来启动
--nolog表示不开启日志
--loglevel=xxx  -s name=xxx


如何加载setting模块，使用import_module然后再dir加载具体的内容

self.crawler.settings.get('name')   可以获取中指令中加载的setting和原setting设置
"""



"""
垂直爬虫，即特定领域的爬虫。垂直爬虫是垂直搜索引擎的核心
垂直搜索引擎，针对某一行业的专业搜索引擎方式
垂直引擎工作：互联网-》网络爬虫-》网页库-》索引模块-》索引库-》用户查询-》服务用户
搜集信息：利用爬虫对某一垂直领域进行广度爬取
整理信息：可以理解为建立索引，保存搜集的信息是肯定的，按某种规则进行排列
接收查询：用户发出查询请求，返回结果
按工作方式可分为三类：全文搜索、目录索引类搜索、元搜索
全文搜索可细分两种：一是有自己的检索程序，为自身数据尽力索引数据库。另一种是调用其他数据库实现
目录索引类，是按类别进行分类，允许没有搜索关键字
元搜索的意思是没有建索引数据库吗，接受用户请求同时进行访问其他搜索引擎
正排索引，倒排索引
正排索引的索引表结构包含三部分：文档的编号、文档中的字和该字的位置，其中文档编号为关键字。每次检索都需要扫描全部的文档？
倒排索引，则采用文档中的子或者词作为关键字进行索引，

"""