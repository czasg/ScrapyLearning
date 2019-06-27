# from whoosh.index import create_in
# from whoosh.fields import *
#
#
# schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
# ix = create_in("temp", schema)
# writer = ix.writer()  # 获取游标
# writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")  # 添加文本
# writer.add_document(title=u"Second document", path=u"/b", content=u"The second one is even more interesting!")
# writer.add_document(title=u"这是一个标题", path=u"/b", content=u"这是中文的文本内容")
# writer.commit()  # 提交文本
# from whoosh.qparser import QueryParser  # 查询类
# with ix.searcher() as searcher:
#     query = QueryParser("content", ix.schema).parse("first")
#     results = searcher.search(query)
#     print(results[0])


import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from IPython.core.display import display, HTML
import json

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 创建schema, stored为True表示能够被检索
schema = Schema(title=TEXT(stored=True, analyzer=analyzer), path=ID(stored=False),
                content=TEXT(stored=True, analyzer=analyzer))

# 存储schema信息至'indexdir'目录下
ix_path = 'temp/'
ix_name = 'test_index_name'


if not os.path.exists(ix_path):
    os.mkdir(ix_path)
ix = create_in(ix_path, schema,indexname=ix_name)

ix.close()



# 这就是增加索引了吗 #
from whoosh.filedb.filestore import FileStorage
#
storage = FileStorage(ix_path)  # idx_path 为索引路径
ix = storage.open_index(indexname=ix_name)
# # 按照schema定义信息，增加需要建立索引的文档
# # 注意：字符串格式需要为unicode格式
with ix.writer() as w:
    # from whoosh.writing import AsyncWriter
    # writer = AsyncWriter(ix,delay=0.25)
    w.add_document(title=u"第一篇文档", path=u"/a", content=u"这是我们增加，的第一篇文档")
    w.add_document(title=u"第二篇文档，呵呵", path=u"/b", content=u"这是我们增加的第二篇文档，哈哈")
    w.add_document(title=u"帅哥，呵呵", path=u"/b", content=u"帅哥，哈哈")

ix.close()

with storage.open_index(indexname=ix_name).searcher() as searcher:
    # 检索标题中出现'文档'的文档
    results = searcher.find(u"content", u"文档")
    # 检索出来的第一个结果，数据格式为dict{'title':.., 'content':...}
    for r in results:
        display(HTML('<h3>' + r.get('title') + '</h3>'))
        display(HTML(r.highlights("content")))  # 高亮标题中的检索词
        print(r.score)  # 分数
        print(r.docnum)

        doc = r.fields()
        jsondoc = json.dumps(doc, ensure_ascii=False)
        display(jsondoc)  # 打印出检索出的文档全部内容


