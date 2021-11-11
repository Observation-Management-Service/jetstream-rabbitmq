#!/usr/bin/env python
import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

credentials = pika.PlainCredentials('briedel', '2QfKHusafBn2zw9S')
parameters = pika.ConnectionParameters('rabbitmq.api.jetstream.rr.icecube.aq',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

consumer = channel.consume('book_test')

for method_frame, properties, body in consumer:
    # Display the message parts and acknowledge the message
    print(method_frame)
    print(properties)
    print(body)
    print(consumer)
    channel.basic_ack(method_frame.delivery_tag)

    # Escape out of the loop after 10 messages
    if method_frame.delivery_tag == 10:
        break

print(" [x] Sent 'Hello World!'")

connection.close()