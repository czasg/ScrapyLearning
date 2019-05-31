__FILE__ = "NOTE BOOK"

"""
通过在scrapy命令行中输入-s key=value，则可以在爬虫中使用self.crawler.settings.get("key")的方式获取

scrapy中response.request就是代表一个Request对象，且是上一级的请求对象。而response.request.callback则是指接受此response对象的函数
或者使用yield response.request.replace(url=new_page, dont_filter=True)，这种scrapy会默认附带我们需要的其他参数嘛
response.request.body.decode()这个好像是代表访问的url
yield Request(url).replace(meta={"url":url})可以使用这种方式传递meta，很强页很骚

request payload请求方式，传送数据是json，需要使用Request(self.url, body=json.dumps(data), method="POST", headers=headers)，头为"application/json;charset=UTF-8"

handle_httpstatus_list = [521, 404] 这是一个scrapy自带的中间件模块里的属性，允许该类型的状态码通过而不是直接过滤
"""