import jieba
import re

"""
这玩意能用来做检索器
"""
test1 = jieba.cut('today is a nice day', cut_all=True)
test2 = jieba.cut('小红今天我们还去以前经常去的地方远足吗？要不咱们换个地方吧！园小园怎么样?没问题小豆芽', cut_all=True)  # 全模式
test3 = jieba.cut('小红今天我们还去以前经常去的地方远足吗？要不咱们换个地方吧！园小园怎么样?没问题小豆芽', cut_all=False)  # 精确模式，默认为此模式
test4 = jieba.cut_for_search('小红今天我们还去以前经常去的地方远足吗？要不咱们换个地方吧！园小园怎么样?没问题小豆芽')  # 搜索引擎模式
test5 = jieba.lcut('中国裁判文书网')
test6 = jieba.lcut('scrapy、个人学习、快乐风男，快乐风男不快乐')
test7 = jieba.lcut('中华人名共和国是一个伟大的国家')
test8 = jieba.lcut('弑神武器')
test9 = jieba.lcut('123')
# print(test9)

article = [{"id1": "Scrapy源码学习一关于源码的学习、个人、开心就好"},
           {"id2": "前端炸裂js特效"},
           {"id3": "个人博客，欢迎光临"},
           {"id4": "(前)端*炸$#!~裂js:|特<>效?特效"}]
# invertedIndex = {'key1': ['id1', 'id2'],
#                  'key3': ['id3', 'id4'],
#                  'key4': ['id5', 'id6'],
#                  'key5': ['id7', 'id8']}

invertedIndex = {}
reObj = re.compile('[()（）~!@#$%^&*_+-=/,.;\'、{}\[\]":<>|?。，：“”]')
for i in article:
    for k,v in i.items():
        for key in set(jieba.lcut(reObj.sub('', v))):
            val = invertedIndex.get(key) or []
            val.append(k)
            invertedIndex[key] = val

# print(invertedIndex)

