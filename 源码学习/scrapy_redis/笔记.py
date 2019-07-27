__file__ = '笔记'

"""
scrapy-redis重写了三个模块：Schedule调度器、Spider爬虫、Pipeline管道

要实现分布式爬虫，需要维护一个共同的消息队列，实现数据上的共享
原生scrapy消息队列是在内存中，重写之后，使用redis数据库作为此容器

首先是调度器，
重写消息队列，也就是创建redis连接
重写过滤机制，也就是使用redis的set集合实现过滤，添加已有元素会返回0，以此为依据进行判断是否过滤
实现了三种消息队列：
FIFO：先进先出队列，
PRIORITY：优先级队列，通过redis的打分zadd集合
LIFO：后进先出队列，通过维护一个双向列表，进行rpop或者lpop

爬虫，
原生爬虫，从start_requests开始，作为数据的入口，，默认使用start_urls存储入口连接。那么我们实现分布式的话肯定不能继续从这里提取自定义的数据了，我们需要提取公共数据
如何提取公共数据，那我们就必须要实现入口的数据，来源于redis即可。
重写start_requests函数，将爬虫调度的渠口，指向redis服务器，也就是数据的来源是redis，而不是自定义的Request或者FormRequest

管道，
这个是一个可选项，将解析出来的item数据，可以从新退回redis，由对应的master进行后序处理
"""
#todo，scrapy的消息机制是如何实现的呢