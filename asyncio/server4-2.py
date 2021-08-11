# server4-2.py
import asyncio

HOST = ''
PORT = 8080


# 데이터 송신
async def send(writer):
    message = input(">>>").encode('utf-8')
    writer.write(message)
    await writer.drain()


# 데이터 수신
async def recv(reader):
    data = await reader.read(1024)
    print(f"Client: {data.decode('utf-8')}")


async def handler(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f'Client: {addr}')

    while True:
        await send(writer)
        await recv(reader)


async def mainServer():
    server = await asyncio.start_server(handler, HOST, PORT)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running')
        task = loop.create_task(mainServer())
    else:
        print('Starting new event loop')
        asyncio.run(mainServer())
