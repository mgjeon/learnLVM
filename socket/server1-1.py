# server1-1.py
import socket

HOST = ''
PORT = 8080

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((HOST, PORT))
serverSock.listen(1)

print(f'Waiting connection from {PORT} port')
connectionSock, addr = serverSock.accept()
print(f'Connected from {addr}')

# 무한 반복문
# 사용자 입력 데이터 전송 -> 클라이언트 데이터 수신
while True:
    sendData = input('>>>')
    connectionSock.send(sendData.encode('utf-8'))

    recvData = connectionSock.recv(1024)
    print('Client: ', recvData.decode('utf-8'))
