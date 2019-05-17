from czaSpider.dataBase.mongo_database.models import Mongodb
from czaSpider.dataBase.mongo_database.orm import get_mongo_client


if __name__ == '__main__':
    if get_mongo_client():
        cza = Mongodb('test', 'hello-mongo')
        # print(cza.source.docs)  # todo, docs -- SUCCESS
        # print(cza.source.find(ne={"isok":False}).documents) # todo, find,documents -- SUCCESS
        # print(cza.source.findAll(field={"_id":1}).documents)  # todo, findAll -- SUCCESS
        # print(cza.source.pop(name='test1', db='redis').documents)  # todo, pop -- success
        # print(cza.source.update(name='test1', set={'age':20}).docs)
        # print(cza.source.updateAll(name='test1', set={"age":100}).docs)
        # print(cza.source.insert(name='test1', db='redis', age=30, isok=True).docs)  # todo, insert -- SUCCESS
        # print(cza.source.insertAll([{"name":"test5"}, {"name":"test6"}]).docs)
        # print(cza.source.removeAll(name='test1').docs)
        # cza.source.update(name="czaOrz", set={"name":"czaOrz", "hello":"world", "py":"mongo", "what":"do not cover?"})  # todo, update -- SUCCESS
        # cza.source.drop()


