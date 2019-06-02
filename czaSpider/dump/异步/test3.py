import time
import asyncio

def waste(x):
    time.sleep(x)
    return "hello"

async def main(loop):
    future1 =  loop.run_in_executor(None, waste, 1)
    print(future1)
    future2 =  loop.run_in_executor(None, waste, 2)
    print(future2)
    future3 =  loop.run_in_executor(None, waste, 3)
    print(future3)
    print("start")
    r3 = await future3
    print(r3)
    r1 = await future1
    print(r1)
    r2 = await future2
    print(r2)

    print(r1, r2, r3)
    return "done!"

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.stop()


def aaaa():
    loop = asyncio.get_running_loop()
    def blocking_io():
        with open("test.file", "rb") as f:
            res = f.read()
    def cpu_bound():
        return sum(i**i for i in range(10*10*10*10))
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    with ThreadPoolExecutor as pool:
        res = await loop.run_in_executor(pool, blocking_io)

    with ProcessPoolExecutor as pool:
        res = await loop.run_in_executor(pool, cpu_bound)