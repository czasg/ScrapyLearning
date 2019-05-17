from czaSpider.dataBase.mongo_database.models import Mongodb
from czaSpider.dataBase.mongo_database.orm import get_mongo_client


if __name__ == '__main__':
    if get_mongo_client():
        cza = Mongodb('test', 'hello')
        # cza.resolver()
        # print(cza.source.docs)  # todo, docs -- SUCCESS
        # print(cza.source.find(name='test5', py='redis', gt={"age":25}).documents) # todo, find,documents -- SUCCESS
        print(cza.source.findAll(field={"_id":1, "py":1, "hello":1}).documents)
        print(cza.source.findAll(field={"_id": 1}).documents)
        # print(cza.source.insert(name='test5', py='redis', age=30).docs)  # todo, insert -- SUCCESS
        # cza.source.update(name="czaOrz", set={"name":"czaOrz", "hello":"world", "py":"mongo", "what":"do not cover?"})  # todo, update -- SUCCESS


