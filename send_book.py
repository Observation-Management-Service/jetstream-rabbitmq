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
channel.queue_declare(queue='book_test')

with open("book", "r") as b:
    for l in b.readlines():
        l = l.strip()
        print(l)
        channel.basic_publish(exchange='',
            routing_key='book_test',
            body=l.encode("utf-8"))
connection.close()
