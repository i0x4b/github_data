import json
import pika
import requests
import sys
from hurry.filesize import size
from settings import RABBITMQ_HOST


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def send_message(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)

        channel.basic_publish(exchange='',
                              routing_key='task_queue_2',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))

        print('-> \'{0}\''.format(message))

        connection.close()
    except:
        send_message(message)


def download_file(url, destination, verbose=False):
    filename = str(url).split("/")[-1]
    if verbose:
        print("attempting to download %s" % filename)
    with open(destination + ("%s" % filename), "wb") as f:
        r = requests.get(url, stream=True)
        l = r.headers.get('content-length')

        if l is None:
            f.write(r.content)
        else:
            dl = 0
            l = int(l)
            for data in r.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / l)
                done2 = int(100 * dl / l)

                sys.stdout.write("\r%s\t\t|%s%s| %s%%\t\t(%s/%s)" % (
                    filename, '=' * done, ' ' * (50 - done), str(done2).zfill(3), size(dl), size(l)))
                sys.stdout.flush()
        sys.stdout.write("\n")
