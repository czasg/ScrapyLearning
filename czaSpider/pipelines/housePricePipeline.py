class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        res = dict(item.copy())
        print('housePrice')
        return None
        # try:
        #     spider.collection.insert_one(res)
        # except:
        #     raise ValueError("insert error")
        # else:
        #     print("insert done")
        # finally:
        #     return item

"""
class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        res = dict(item.copy())
        return item
        
        sql = "create table "
        sql = "insert " 

problem: how to analyse and increase data?
"""