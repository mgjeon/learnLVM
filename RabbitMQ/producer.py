# producer.py
import pika

# localhost에 설치된 RabbitMQ 서버에 연결한다.
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# hello라는 이름의 Queue를 생성한다.
channel.queue_declare(queue='hello')

# 전송할 메시지를 입력한다.
message = 'Hello World!'

# exchange에 빈 문자열을 입력하여 기본 Exchange를 사용한다.
# 메시지가 저장되야 하는 Queue 이름을 routing_key에 입력한다.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
print(f"Sent: {message}")

# 연결을 종료한다.
connection.close()
