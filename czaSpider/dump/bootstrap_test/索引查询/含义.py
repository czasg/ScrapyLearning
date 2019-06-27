__file__ = '意义'

"""
搜索引擎：
搜索器：也就是爬虫
索引器：
索引数据库：
检索器：
用户接口：

首先爬虫将获取到的DOM文本进行抓取并清洗，获取具有一定价值的信息。有广度优先（爬完当前页所有连接，再转而下一链接中的链接，scrapy就是这样的）、深度优先（某一个链接爬完为止）

然后是索引器，其功能就是理解搜索器中获取到的有用信息，从中抽取出索引项（属性），生成倒排索引文件，进而建立索引数据库
倒排索引即由索引项查找相对应的文档
索引项有客观索引项和内容索引项
举例：
数据库有table，3男2女，年龄分别为15,15,17,18,18
针对性别做倒排索引
性别  编号
男    1,3,5
女    2,4

针对年龄做索引
年龄  编号
15    1,2
17    3
18    4,5



"""

"""好文章
https://wenku.baidu.com/view/3b38bc95a0c7aa00b52acfc789eb172ded6399f3.html?from=search
"""