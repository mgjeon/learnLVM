# client1-2.py
import socket


def send(sock):
    sendData = input('>>>')
    sock.send(sendData.encode('utf-8'))


def receive(sock):
    recvData = sock.recv(1024)
    print('Server: ', recvData.decode('utf-8'))


HOST = '127.0.0.1'
PORT = 8081

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
print('Connection OK')

while True:
    receive(clientSocket)
    send(clientSocket)
