import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('127.0.0.1', 27017)

db = client['housePrice']
collection = db['ziru_housePriceColl20190414']

async def test():
    count = await collection.count_documents({})
    print(count)
    pass


loop = asyncio.get_event_loop()
loop.run_until_complete(test())





