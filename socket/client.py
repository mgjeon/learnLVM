# client.py
import socket

# HOST는 접속할 서버의 IP주소, PORT는 포트번호이다.
# 여기서는 localhost를 사용한다.
HOST = '127.0.0.1'
PORT = 8080

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 선언한 HOST와 PORT를 통해 서버에 접속한다.
clientSock.connect((HOST, PORT))
print('Connection OK')

# 서버에게 데이터 전송
clientSock.send('I am a client'.encode('utf-8'))
print('Client --Message--> Server')

# 서버로부터 데이터 수신
data = clientSock.recv(1024)
print('Received Data: ', data.decode('utf-8'))
