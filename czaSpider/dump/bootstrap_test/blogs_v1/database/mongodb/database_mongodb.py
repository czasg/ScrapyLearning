import pymongo, time


class Mongodb:
    client = None

    @classmethod
    def get_client(cls):
        cls.client = pymongo.MongoClient()
        return cls()

    def insert_mongodb(self, attr, snow_key, to, message, state=0, **kwargs):
        doc = {'message': message, 'state': state, 'info_from': snow_key, 'time': int(time.time())}
        doc.update(kwargs)
        self.client[attr][to].insert_one(doc)


mongodb_handler = Mongodb.get_client()
