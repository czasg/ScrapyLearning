import time
import json
import pandas as pd


def mongodb2csv(spider, source=False, resolver=False):
    mongodb = spider.mongo.source if source else spider.mongo.resolver if resolver else None
    df = pd.DataFrame(mongodb.findAll().documents)
    df.to_csv('mongodb2csv-{}{}.csv'.format(spider.name, int(time.time())))
    print('Mongodb transform to CSV SUCCESS!')


def mongodb2json(spider, source=False, resolver=False, dropColumn=''):
    mongodb = spider.mongo.source if source else spider.mongo.resolver if resolver else None
    documents = mongodb.findAll().documents
    if dropColumn:
        for doc in documents:
            doc.pop(dropColumn)
    with open('%s-%s.json' % (spider.collName, spider.dbName), 'w', encoding='utf-8') as f_w:
        f_w.write(json.dumps(documents, ensure_ascii=False))
    print('Mongodb transform to JSON SUCCESS!')