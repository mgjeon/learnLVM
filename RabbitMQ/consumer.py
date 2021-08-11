# consumer.py
import pika

# localhost에 설치된 RabbitMQ 서버에 연결한다.
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# hello라는 이름의 Queue를 생성한다.
channel.queue_declare(queue='hello')


# Queue를 subscribe할 callback함수를 생성한다.
def callback(ch, method, properties, body):
    print(f"Recevied: {body}")


# RabbitMQ에게 사용할 Queue의 이름과, 사용할 callback함수의 이름을 알려준다.
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

# 필요할 때마다 callback함수를 실행시키는 무한루프에 진입한다.
print('Waiting for messages.')
channel.start_consuming()
