# client2.py
import socket
import threading
import time
import asyncio
import sys

async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

async def send(sock):
    while True:
        print('send')
        sendData = await ainput('>>>')
        sock.send(sendData.encode('utf-8'))
        await asyncio.sleep(0)


async def receive(sock):
    while True:
        print('recv')
        recvData = sock.recv(1024)
        print('Server: ', recvData.decode('utf-8'))
        await asyncio.sleep(0)


HOST = '127.0.0.1'
PORT = 8080

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((HOST, PORT))
print('Connection OK')

# sender = threading.Thread(target=send, args=(clientSock,))
# receiver = threading.Thread(target=receive, args=(clientSock,))

# sender.start()
# receiver.start()

# while True:
#     time.sleep(1)
#     pass

async def main():
    await asyncio.gather(send(clientSock), receive(clientSock))

asyncio.run(main())
# loop = asyncio.get_event_loop()
# loop.create_task(send(clientSock))
# # print("send start")
# loop.create_task(receive(clientSock))
# # print("receive start")
# loop.run_forever()