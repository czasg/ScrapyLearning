import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(message)
        await websocket.send('Are You Ok')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8080))
asyncio.get_event_loop().run_forever()