# server1-2.py
import socket


def send(sock):
    sendData = input('>>>')
    sock.send(sendData.encode('utf-8'))


def receive(sock):
    recvData = sock.recv(1024)
    print('Client: ', recvData.decode('utf-8'))


HOST = ''
PORT = 8081

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((HOST, PORT))
serverSock.listen(1)

print(f'Waiting connection from {PORT} port')
connectionSock, addr = serverSock.accept()
print(f'Connected from {addr}')

while True:
    send(connectionSock)
    receive(connectionSock)
