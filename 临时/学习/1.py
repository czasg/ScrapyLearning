import asyncio
import aiohttp
import time

loop = asyncio.get_event_loop()


async def fetch():
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('http://www.baidu.com') as response:
            # print(await response.read())
            """No Thing"""


async def multi_fetch():
    tasks = [asyncio.create_task(fetch()) for _ in range(10)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time.time()
    loop.run_until_complete(fetch())
    # loop.run_until_complete(multi_fetch())
    print(time.time() - start)
