# client4-2.py
import asyncio

HOST = '127.0.0.1'
PORT = 8080


# 데이터 송신
async def send(writer):
    message = input(">>>").encode('utf-8')
    writer.write(message)
    await writer.drain()


# 데이터 수신
async def recv(reader):
    data = await reader.read(1024)
    print(f"Server: {data.decode('utf-8')}")


async def mainClient():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
    except OSError:
        print('Connection fail')
        return

    while True:
        await recv(reader)
        await send(writer)


if __name__ == "__main__":

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running')
        tsk = loop.create_task(mainClient())
    else:
        print('Starting new event loop')
        asyncio.run(mainClient())
