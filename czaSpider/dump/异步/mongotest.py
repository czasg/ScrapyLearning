import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('127.0.0.1', 27017)

db = client['housePrice']
collection = db['ziru_housePriceColl20190414']

async def test():
    count = await collection.count_documents({})
    print(count)
    pass

async def api_get_boss_salary_statistic():
    res = {}
    dbNames_and_collectionNames = [{'job': 'boss'}]
    for di in dbNames_and_collectionNames:
        for dbName, collectionName in di.items():
            collection = client[dbName][collectionName]
            column = 'job_salary'
            documents = collection.find({}, {column: 1})
            async for doc in documents:
                print(doc)
    return res


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
