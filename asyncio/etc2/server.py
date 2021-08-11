import asyncio    
    
async def handle_asyncclient(reader, writer):
    print('client :', writer.get_extra_info('peername'))
    while True:
        data = await reader.read(8)
        if data == b'ping':
            writer.write(b'pong')
            await writer.drain()
            print('recv: ping -> send: pong')
        elif data == b'done':
            print('recv: done')
            break
        elif len(data) == 0:
            break
    
    writer.close()
    await writer.wait_closed()
    print('connection was closed')
    
async def server_asyncmain():
    server = await asyncio.start_server(handle_asyncclient,'localhost',8000)  
    if server is not None:
        print('server started')
        #
        await asyncio.sleep(60)
        server.close()
        await server.wait_closed()
        print('server was closed')


if __name__ == "__main__":
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        print('Async event loop already running')
        tsk = loop.create_task(server_asyncmain())
    else:
        print('Starting new event loop')
        asyncio.run(server_asyncmain())   