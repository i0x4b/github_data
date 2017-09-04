import sys

import pika

from helpers.command import Command
from settings import RABBITMQ_QUEUE, RABBITMQ_HOST, RUN_DOWNLOAD, RUN_FILE_PROCESSING, WATCH_DATA


def start_master():
    def download_data(year, month, day, hour):
        month = str(month).zfill(2)
        day = str(day).zfill(2)
        url = "http://data.githubarchive.org/%d-%s-%s-%d.json.gz" % (year, month, day, hour)

        command = Command("download_file", url)
        command.execute()

    def read_data(year, month, day, hour):
        month = str(month).zfill(2)
        day = str(day).zfill(2)
        filename = "data/%d-%s-%s-%d.json.gz" % (year, month, day, hour)

        command = Command("parse_file", filename)
        command.execute()

    def watch_queue():
        last_message_count = 1

        try:
            while last_message_count > -1:
                connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
                channel = connection.channel()

                channel.exchange_declare(exchange=RABBITMQ_QUEUE, type='fanout')

                queue = channel.queue_declare(queue='task_queue_2', durable=True)
                last_message_count = queue.method.message_count
                sys.stdout.write("\rMessages left: %d" % last_message_count)
                sys.stdout.flush()

                connection.close()

                if last_message_count == 0:
                    done()
        except:
            watch_queue()

    def done():
        print("We're done!")
        exit(0)

    if RUN_DOWNLOAD:
        for y in range(2015, 2016):
            for m in range(6, 12):
                for d in range(1, 28):
                    for h in range(0, 24):
                        download_data(y, m, d, h)

    if RUN_FILE_PROCESSING:
        for y in range(2015, 2016):
            for m in range(6, 12):
                for d in range(1, 28):
                    for h in range(0, 24):
                        read_data(y, m, d, h)

    if WATCH_DATA:
        watch_queue()
