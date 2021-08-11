# server.py
import socket

# HOST는 Hostname, IP주소, 빈 문자열('')이 될 수 있다.
# 빈 문자열('')은 INADDR_ANY를 의미하며, 모든 네트워크 인터페이스에서의 접속 허용을 뜻한다.
HOST = ''
# PORT는 1-65535 사이의 숫자가 될 수 있다.
# 클라이언트의 접속을 기다리는 포트 번호이다.
PORT = 8080

# AF(Address Family)로 IPv4, 소켓 타입으로 TCP를 사용하는 소켓을 생성한다.
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind()와 listen()은 서버 소켓을 만들 때만 필요하다.
# 생성된 소켓에 AF를 연결한다.
serverSock.bind((HOST, PORT))
# 클라이언트의 접속을 대기한다.
# 동시접속수는 1로 제한한다.
serverSock.listen(1)

# accept()는 서버 소켓을 만들 때만 필요하다.
# 클라이언트의 접속이 이루어질 때까지 이 부분에서 프로그램 실행이 중단된다.
# 접속이 이루어지면 새로운 소켓과 클라이언트의 AF를 return한다.
print(f'Waiting connection from {PORT} port')
connectionSock, addr = serverSock.accept()
print(f'Connected from {addr}')

# accpet()를 통해 생성된 소켓을 통해 데이터 송수신이 가능하다
# serverSock은 계속해서 외부로부터의 접속을 기다리는 소켓이고,
# connectionSock은 클라이언트 접속이 수립되었을 때 생기는 일시적 소켓이다.

# 1024 byte씩 끊어서 데이터를 수신하며, utf-8로 디코딩하여 출력한다.
data = connectionSock.recv(1024).decode('utf-8')
print(f'Received Data : {data}')

# 문자열 데이터를 utf-8로 인코딩하여 클라이언트에게 송신한다.
connectionSock.send("I am a server".encode('utf-8'))
print('Server --Message--> Client')
