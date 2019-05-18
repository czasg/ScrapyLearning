import time
import pandas as pd


def mongodb2csv(spider, source=False, resolver=False):
    mongodb = spider.mongo.source if source else spider.mongo.resolver if resolver else None
    df = pd.DataFrame(mongodb.findAll().documents)
    df.to_csv('mongodb2csv-{}{}.csv'.format(spider.name, int(time.time())))
    print('Mongodb transform to CSV SUCCESS!')
