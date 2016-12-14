import json
import os

import pika
from bson import BSON
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

if 'FEATURES' in os.environ:
    features = os.environ['FEATURES'].split(':')

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}
mongoCred = {'uri': 'mongodb://clodes3:TopCPSKek@baprof.net/clodes3'}

# Connect to Mongo
client = MongoClient(mongoCred['uri'])
frames_collection = client['clodes3']['frames']
frames_collection.create_index('id', unique=True)
rects_collection = client['clodes3']['rects']
rects_collection.create_index('id', unique=True)


def on_new_image(ch, method_frame, header_frame, body):
    msg = BSON.decode(body)
    print("Got frame {}".format(msg['id']))
    try:
        frames_collection.insert(msg)
    except DuplicateKeyError:
        pass
    ch.basic_ack(delivery_tag=method_frame.delivery_tag)


def on_new_rect(ch, method_frame, header_frame, body):
    msg = BSON.decode(body)
    try:
        rects_collection.insert(msg)
    except DuplicateKeyError:
        pass
    ch.basic_ack(delivery_tag=method_frame.delivery_tag)


def subscribe_to_topic(ch, topic, callback):
    queue = "train_data_recorder.{}".format(topic)
    ch.queue_declare(queue=queue)
    ch.queue_bind(exchange='amq.topic', queue=queue, routing_key=topic)
    ch.basic_consume(consumer_callback=callback, queue=queue)


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()

subscribe_to_topic(channel, 'image.new', on_new_image)
subscribe_to_topic(channel, 'rects.new.*', on_new_rect)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print('Starting to synchronously consume messages')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
