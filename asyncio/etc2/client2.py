import asyncio
_port = 7771

async def pingpong_client():
    #open_connection() 코루틴은 주어진 호스트, 
    # 포트 정보를 통해 서버와 연결을 수립하고, 
    # 연결이 의존하는 소켓을 제거할 수 있는 (reader, writer) 객체 쌍을 리턴합니다. 
    # 클라이언트 구현 코드에서는 이 스트림 객체들을 사용해서 서버와 통신하면 됩니다.
    # 간단한 tcp 에코 통신을 위한 비동기 클라이언트를 만들어보겠습니다. 
    # 클라이언트의 동작은 크게 4단계로 나눠집니다. 
    # 1) 서버와 연결하고 스트림을 생성합니다. 
    # 2) 쓰기 스트림을 통해 데이터를 전송합니다. 
    # 3) 서버로부터 응답을 기다리고, 읽습니다. 
    # 4) 소켓(스트림)을 닫습니다.
    try:
        reader, writer = await asyncio.open_connection(host='localhost',port=_port)
    except OSError:
        print('connection fail')
        return

    while True:
        line = input("[C] enter message: ")
        payload = line.encode()
        writer.write(payload)
        await writer.drain()
        print(f"[C] sent: {len(payload)} bytes.\n")
        data = await reader.read(1024)  # type: bytes
        print(f"[C] received: {len(data)} bytes")
        print(f"[C] message: {data.decode()}")


if __name__ == "__main__":
     asyncio.run(pingpong_client())