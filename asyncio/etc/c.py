import asyncio
from random import random

_port = 7770
# asyncio socket server/client


async def run_client(host: str, port: int):
    # 서버와의 연결을 생성합니다.
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(host, port)

    # show connection info
    print("[C] connected")

    # 루프를 돌면서 입력받은 내용을 서버로 보내고,
    # 응답을 받으면 출력합니다.
    while True:
        line = input("[C] enter message: ")
        if not line:
            break

        # 입력받은 내용을 서버로 전송
        payload = line.encode()
        writer.write(payload)
        await writer.drain()
        print(f"[C] sent: {len(payload)} bytes.\n")

        # 서버로부터 받은 응답을 표시
        data = await reader.read(1024)  # type: bytes
        print(f"[C] received: {len(data)} bytes")
        print(f"[C] message: {data.decode()}")

    # 연결을 종료합니다.
    print("[C] closing connection…")
    writer.close()
    await writer.wait_closed()


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        # 클라이언트가 보낸 내용을 받기
        data: bytes = await reader.read(1024)
        # 받은 내용을 출력하고,
        # 가공한 내용을 다시 내보내기
        peername = writer.get_extra_info('peername')
        print(f"[S] received: {len(data)} bytes from {peername}")
        mes = data.decode()
        print(f"[S] message: {mes}")
        res = mes.upper()[::-1]
        await asyncio.sleep(random() * 2)
        writer.write(res.encode())
        await writer.drain()


async def run_server():
    # 서버를 생성하고 실행
    server = await asyncio.start_server(handler, host="127.0.0.1", port=_port)
    async with server:
        # serve_forever()를 호출해야 클라이언트와 연결을 수락합니다.
        await server.serve_forever()


async def main():
    await asyncio.wait([asyncio.create_task(run_server()), asyncio.create_task(run_client("127.0.0.1", _port))])


if __name__ == "__main__":
    asyncio.run(main())