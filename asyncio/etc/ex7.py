import asyncio
from aioconsole import ainput

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_coros())


async def start_coros():
    # ensure_future -> create_task in Python 3.7
    tasks = [asyncio.ensure_future(coro()) for coro in (coro1, coro2)]
    await asyncio.wait(tasks)


async def coro1():
    # print("coro1")
    # await asyncio.sleep(3000)
    a = await ainput(">>>")
    print(a)


async def coro2():
    print("coro2 - we want to get here")
    await asyncio.sleep(1000)


if __name__ == "__main__":
    main()