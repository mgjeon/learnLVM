from contextlib import suppress
import asyncio


async def wait(t):
    await asyncio.sleep(t)
    return t


async def raising_wait(t):
    await asyncio.sleep(t)
    raise TimeoutError("You waited for too long, pal")


loop = asyncio.new_event_loop()

done_first, pending = loop.run_until_complete(
    asyncio.wait(
        {wait(1), raising_wait(2), wait(3)}, return_when=asyncio.FIRST_COMPLETED
    )
)

for coro in done_first:
    try:
        print(coro.result())
    except TimeoutError:
        print("cleanup after error before exit")

for p in pending:
    p.cancel()
    with suppress(asyncio.CancelledError):
        loop.run_until_complete(p)

loop.close()