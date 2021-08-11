import asyncio
_port = 7770

# 서버의 경우에는 asyncio.start_server() 코루틴을 사용하여 생성합니다. 
# 소켓 서버는 기본적으로 런루프를 기반으로 싱글스레드에서 여러 클라이언트의 요청을 처리할 수 있도록 합니다. 
# 셀렉터를 사용한 멀티 플렉싱 예제와 비슷하게, 
# 서버는 생성될 때 요청을 처리할 핸들러를 필요로 합니다. 
# start_server() 함수의 첫 인자는 요청을 처리하는 핸들러이며, 
# 다시 이 핸들러는 소켓을 다루기 때문에 (StreamReader, StreamWriter) 쌍을 인자로 받게 됩니다.
# start_server() 함수는 다시 내부적으로 현재 런루프의 loop.create_server() 메소드를 호출하여 
# 서버를 생성합니다. 이 함수는 asyncio.Server의 인스턴스 객체를 리턴합니다. 
# 생성된 서버 객체는 비동기 컨텍스트 관리자로 async with 절을 시작할 수 있습니다. 
# with 절이 끝나면 서버가 닫히고 더 이상 연결을 받아들이지 않는 것이 보장됩니다. 
# 참고로 서버의 속성은 다음과 같이 정리합니다.
# sockets : 서버가 리스닝하는 소켓의 리스트
# is_serving() : 서버가 연결을 받는지
# close() : 서버를 닫습니다. 실제 닫히는 것을 보장하려면 wait_closed() 와 함께 사용합니다.
# ↱ wait_closed() : 서버가 완전히 닫힐 때까지 대기합니다.
# get_loop() : 서버가 사용하는 이벤트 루프를 리턴합니다.
# ↱ start_serving() : 연결을 받기 시작합니다. 이미 시작한 후에 호출해도 안전합니다.
# ↱ serve_forever() : 연결을 받기 시작하며, 코루틴이 취소될때까지 계속합니다. 
# 서버 객체는 생성 후 start_serving() 이나 serve_forever()를 호출하여 연결 수락을 시작할 수 있습니다. 
# 앞에서도 말했지만 async with 절 내에서 시작하는 것이 좋습니다.

# 그런데 서버는 연결을 받기만 할 뿐, 실제 처리는 핸들러에게 위임합니다. 핸들러 연결이 수락되어 소켓이 생성되면, 해당 소켓을 사용하여 클라이언트와 통신하는 과정을 수행합니다. 
# 따라서 핸들러는 다시 읽기/쓰기 스트림을 인자로 받는 코루틴함수이며, 
# 내부 구현은 스트림 리더를 통해서 데이터를 읽고 쓰면 됩니다.
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
        writer.write(res.encode())
        await writer.drain()

async def run_server():
    # 서버를 생성하고 실행
    server = await asyncio.start_server(handler, host="127.0.0.1", port=_port)
    async with server:
        # serve_forever()를 호출해야 클라이언트와 연결을 수락합니다.
        await server.serve_forever()
    
if __name__ == "__main__":
    asyncio.run(run_server())
