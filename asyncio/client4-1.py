# client4-1.py
import asyncio

HOST = '127.0.0.1'
PORT = 8080


async def mainClient():
    # 주어진 host, port를 가지고 서버와 연결하여 (reader, writer) 튜플을 반환한다.
    # reader는 StreamReader 클래스의 인스턴스이다.
    # writer는 StreamWriter 클래스의 인스턴스이다.
    # 서버와 연결에 실패하면 발생하는 OSError를 처리하기 위해 try except 구문을 사용한다.
    try:
        reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    except OSError:
        print('Connection fail')
        return

    for _ in range(10):
        writer.write(b'ping')
        print('send: ping')
        await writer.drain()
        data = await reader.read(8)
        print('recv:', data.decode())
        await asyncio.sleep(1)

    writer.write(b'done')
    await writer.drain()
    print('send: ping')
    writer.close()
    await writer.wait_closed()
    print('Connection was closed')


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running')
        task = loop.create_task(mainClient())
    else:
        print('Starting new event loop')
        asyncio.run(mainClient())
