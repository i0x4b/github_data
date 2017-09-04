import gzip
import json

import pika

from helpers.common import download_file
from settings import RABBITMQ_HOST, RABBITMQ_QUEUE


def start_processor():
    # Start for connection to sub
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_QUEUE, type='fanout')

    channel.queue_declare(queue='task_queue_2', durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        if data['type'] == 'command':
            if data['action'] == 'download_file':
                print("<-- " + data['body'])
                download_file(data['body'], 'data/')
            elif data['action'] == 'parse_file':
                print("<-- C:/Users/aa275/projects/github_data/" + data['body'])
                read_file(data['body'])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def read_file(file):
        data = []
        try:
            for line in gzip.open(file, "rb"):
                data.append(json.loads(line))
        except EOFError:
            print("EOFError on file " + file)
        except FileNotFoundError:
            print("FileNotFoundError on file " + file)

        print("Length: %d" % len(data))

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue='task_queue_2')

    print('standing by to receive. ctrl+c to stop')
    channel.start_consuming()
