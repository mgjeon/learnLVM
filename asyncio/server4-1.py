# server4-1.py
import asyncio

HOST = ''
PORT = 8080


# async def 키워드를 통해 코루틴(coroutine)을 만들 수 있다.
async def handler(reader, writer):
    # 연결된 클라이언트의 주소를 받아온다.
    addr = writer.get_extra_info('peername')
    print(f'Client: {addr}')
    while True:
        # read()는 코루틴으로, 아래의 경우 8바이트를 읽고 결과를 반환한다.
        data = await reader.read(8)
        if data == b'ping':
            # write()는 인자로 받은 데이터를 하부 소켓에 즉시 기록하려 시도한다.
            # 실패하면 기록이 가능할 때까지 데이터는 버퍼에 계류된다.
            # write()는 drain()과 함께 사용해야 한다.
            writer.write(b'pong')
            # drain()은 코루틴으로, 스트림에 기록하는 것이 적절할 때까지 기다린다.
            await writer.drain()
            print('recv: ping -> send: pong')
        elif data == b'done':
            print('recv: done')
            break
        elif len(data) == 0:
            break

    # close()는 스트림과 하부 소켓을 닫는다.
    # close()는 wait_closed()와 함께 사용해야 한다.
    writer.close()
    await writer.wait_closed()
    # wait_closed()는 코루틴으로, 스트림이 닫힐 때까지 기다린다.
    # close() 뒤에서 호출되면 하부 연결이 닫힐 때까지 기다린다.
    print('Connection was closed')


async def mainServer():
    # 주어진 host, port 정보를 가지고 소켓 서버를 시작한다.
    # 새 클라이언트 연결이 이루어질 때마다 handler가 호출된다.
    # handler는 (reader, writer)를 인자로 받는다.
    # handler가 코루틴일 경우 자동으로 Task로 예약된다.
    server = await asyncio.start_server(handler, host=HOST, port=PORT)

    if server is not None:
        print('Server started')
        # 60초 동안 현재 태스크를 중단한다.
        await asyncio.sleep(60)
        server.close()
        await server.wait_closed()
        print('Server was closed')


if __name__ == "__main__":
    # asyncio.run 외의 다른 코드들은 RuntimeError 방지 목적이다.
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running')
        task = loop.create_task(mainServer())
    else:
        print('Starting new event loop')
        # Python 3.7 이상에서 코루틴을 실행하는 함수이다.
        asyncio.run(mainServer())
