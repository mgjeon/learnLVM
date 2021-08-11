import asyncio    

_port = 7771
async def handler(reader, writer):
    print('client :', writer.get_extra_info('peername'))
    while True:
        #asyncio.StreamReader는 IO 스트림에서 데이터를 읽는 API를 제공하는 객체입니다. 
        # 이 클래스는 다음과 같은 속성들을 갖습니다. (↱ 표시가 있으면 코루틴입니다.)
        #최대 n바이트를 읽어들입니다. n이 -1 이면 EOF 까지 읽은 다음, 모
        # 든 바이트를 반환합니다. 
        # 이미 EOF를 수신했고 내부 버퍼가 비어있다면 빈 bytes를 반환합니다.
        data: bytes = await reader.read(1024)
        peername = writer.get_extra_info('peername')
        print(f"[S] received: {len(data)} bytes from {peername}")
        mes = data.decode()
        print(f"[S] message: {mes}")

        #asyncio.StreamWriter</a>는 IO 스트림에 대해 비동기로 바이트를 쓰는 API를 제공합니다. 
        # 특이한 점은 write() 메소드는 일반 함수이며, drain() 코루틴과 함께 쓰여야 한다는 점입니다. 
        # 이는 아마도 버퍼에 기록하는 작업은 즉시 수행하되, 
        # 실제 외부 IO가 일어나는 시점에서 비동기적으로 처리가 되도록 하는 것으로 보입니다.
        line = input("[S] enter message: ")
        payload = line.encode()
        #write(data) : 하부 스트림에 즉시 data를 기록합니다. 
        # 실패하는 경우 data는 보낼 수 있을 때까지 버퍼에 남게 됩니다. 
        # 이는 실제 쓰기 완료를 보장하지 않으므로 ‘즉시 버퍼에 쓴다’는 동작으로 이해해야 하며, 
        # drain() 메소드와 함께 사용해야 합니다. 
        writer.write(payload)
        # 스트림에 기록하는 것이 가능해질 때까지 기다립니다. 
        # write() 메소드가 코루틴이 아닌 blocking callable임에 유의해야 합니다. 
        # 이 메소드는 쓰기 버퍼가 차올라 여유가 없으면 대기하여 동일 코루틴이 버퍼를 손상시키는 것을 막습니다.
        await writer.drain()

async def run_server():
    # 서버를 생성하고 실행
    server = await asyncio.start_server(handler, host="127.0.0.1", port=_port)
    async with server:
        # serve_forever()를 호출해야 클라이언트와 연결을 수락합니다.
        await server.serve_forever()

if __name__ == "__main__":
     asyncio.run(run_server())