__FILE__ = "NOTE BOOK"

"""
通过在scrapy命令行中输入-s key=value，则可以在爬虫中使用self.crawler.settings.get("key")的方式获取

scrapy中response.request就是代表一个Request对象，且是上一级的请求对象。而response.request.callback则是指接受此response对象的函数
或者使用yield response.request.replace(url=new_page, dont_filter=True)
response.request.body.decode()这个好像是代表访问的url

request payload请求方式，传送数据是json，需要使用Request(self.url, body=json.dumps(data), method="POST", headers=headers)，头为"application/json;charset=UTF-8"


"""