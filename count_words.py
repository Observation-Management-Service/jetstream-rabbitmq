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

consumer = channel.consume('book_test', inactivity_timeout=10)
channel.queue_declare(queue='book_test_out')


for method_frame, properties, body_raw in consumer:
    if (method_frame is None) and (properties is None) and (body_raw is None):
        break

    body = body_raw.decode()
    print(body.strip().split(" ")[0])
    if not body.strip().split(" ")[0]:
        channel.basic_ack(method_frame.delivery_tag)
        continue
    newl = []
    for w in body.strip().split(" "):
        if "." in w: w = w.strip(".")
        if "," in w: w = w.strip(",")
        if "\"" in w: w = w.strip("\"")
        newl.append(w)
    print(newl)
    word_count = count_words(newl)
    channel.basic_publish(exchange='',
                      routing_key='book_test_out',
                      body=json.dumps(word_count))
    print(word_count)
    channel.basic_ack(method_frame.delivery_tag)

connection.close()