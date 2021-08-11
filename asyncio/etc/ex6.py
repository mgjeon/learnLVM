import asyncio

async def snmp():
    while True:
        print("Doing the snmp thing")
        await asyncio.sleep(1)

async def proxy():
    while True:
        print("Doing the proxy thing")
        await asyncio.sleep(2)

loop = asyncio.get_event_loop()
loop.create_task(snmp())
loop.create_task(proxy())
loop.run_forever()