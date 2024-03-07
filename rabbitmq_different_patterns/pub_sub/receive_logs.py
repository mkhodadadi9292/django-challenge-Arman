#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('rabbit', 'rabbit')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(
    parameters)
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Once the consumer connection is closed, the queue should be deleted. There's an exclusive flag for that:
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# That relationship between exchange and a queue is called a binding.
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
