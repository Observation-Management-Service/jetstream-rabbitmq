#!/usr/bin/env python
import pika
from collections import Counter
import json

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

def count_words(s: list) -> dict:
    return dict(Counter(s))

credentials = pika.PlainCredentials('briedel', '2QfKHusafBn2zw9S')
parameters = pika.ConnectionParameters('rabbitmq.api.jetstream.rr.icecube.aq',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

consumer = channel.consume('book_test_out', inactivity_timeout=10)


for method_frame, properties, body_raw in consumer:
    if (method_frame is None) and (properties is None) and (body_raw is None):
        break
    print(method_frame.delivery_tag)
    body = body_raw.decode()
    print(body)
    channel.basic_ack(method_frame.delivery_tag)

connection.close()