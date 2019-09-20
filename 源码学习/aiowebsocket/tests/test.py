import asyncio
from aiowebsocket.converses import AioWebSocket


async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator

        # 给服务端发送验证消息，观察网页接口数据动态获取
        message = '{"action":"subscribe","args":["QuoteBin5m:14"]}'
        await converse.send(message)

        while True:
            receive = await converse.receive()

            # 拿到的是byte类型数据，解码为字符串数据
            print(receive.decode())


if __name__ == '__main__':
    # remote = 'wss://api.bbxapp.vip/v1/ifcontract/realTime'
    # asyncio.get_event_loop().run_until_complete(startup(remote))
    # handler = AioWebSocket('').manipulator
    # print(handler)

    remote = 'wss://127.0.0.1:8080'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup(remote))
    loop.run_forever()
