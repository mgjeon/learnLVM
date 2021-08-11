import requests
import asyncio

import time
s = time.time()
results = []

#---------------------- A 파트 ------------------------
async def printH():
    while True:
        print("H")
        await asyncio.sleep(1000)

async def printA():
    while True:
        n = input(">>>")
        print(n)


#---------------------- B 파트 ------------------------ 
async def main():
    fts = [asyncio.create_task(printH()),asyncio.create_task(printA())]
    r = await asyncio.gather(*fts)
    global results
    results = r

#---------------------- C 파트 ------------------------
loop = asyncio.get_event_loop()
loop.schedu
loop.run_until_complete(main())
loop.close
e = time.time()

print(results)
print("{0:.2f}초 걸렸습니다".format(e - s))