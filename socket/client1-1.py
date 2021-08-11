# client1-1.py
import socket

HOST = '127.0.0.1'
PORT = 8080

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((HOST, PORT))
print('Connection OK')

# 무한 반복문
# 서버 데이터 수신 -> 사용자 입력 데이터 송신
while True:
    recvData = clientSock.recv(1024)
    print('Server: ', recvData.decode('utf-8'))

    sendData = input('>>>')
    clientSock.send(sendData.encode('utf-8'))
