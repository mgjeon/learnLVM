# server2.py
import socket
import threading
import time


def send(sock):
    while True:
        sendData = input('>>>')
        sock.send(sendData.encode('utf-8'))


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('Client: ', recvData.decode('utf-8'))


HOST = ''
PORT = 8080

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((HOST, PORT))
serverSock.listen(1)

print(f'Waiting connection from {PORT} port')
connectionSock, addr = serverSock.accept()
print(f'Connected from {addr}')

# 쓰레드가 실행할 함수는 target에 작성한다.
# target 함수에 전달할 인자는 args에 튜플형태로 제공한다.
sender = threading.Thread(target=send, args=(connectionSock,))
receiver = threading.Thread(target=receive, args=(connectionSock,))

# start()를 통해 쓰레드를 시작한다.
# 쓰레드는 일이 끝나면 사라지지만,
# target 함수 내부에 무한 반복문이 있으므로 계속 실행된다.
sender.start()
receiver.start()

# 프로세스가 끝나면 쓰레드가 사라지므로 무한 반복문을 사용한다.
# time 라이브러리를 사용하여 1초 동안 중단되도록 한다.
# 이를 통해 과도한 시스템 자원 낭비를 방지한다.
while True:
    time.sleep(1)
    pass
