import json

# 索引数据库的数据结构，保存为json数据格式，InvertedIndex.json，叫倒排索引数据库
# key为对应的属性标签，后面则为对应的文本
invertedIndex = {'key1': ['id1', 'id2'],
                 'key3': ['id3', 'id4'],
                 'key4': ['id5', 'id6'],
                 'key5': ['id7', 'id8']}

# 索引数据库是额外训练的吗
# 每次更新都是重新删除，重建一个？那会不会太浪费了啊
article = [{"id1": "Scrapy源码学习一关于源码的学习、个人、开心就好"},
           {"id2": "前端炸裂js特效"},
           {"id3": "个人博客，欢迎光临"}]




