import os
import random

import pika
import json

from bson import BSON

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()
input_topic_name = 'image.faces.done'
input_queue_name = 'attendance_aggregator.image.faces.done'
channel.queue_declare(queue=input_queue_name)
channel.queue_bind(exchange='amq.topic', queue=input_queue_name, routing_key=input_topic_name)

# -----------------------------------------------------------------------------

def newImageCallback(channel, method, properties, body):
    decoded = BSON.decode(body)
    print(decoded)

    #output_topic_name = 'rects.classify.done.{}'.format(decoded['feature_name'])
    #channel.basic_publish(routing_key=output_topic_name, exchange='amq.topic', body=BSON.encode(msg))
    channel.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(newImageCallback, queue=input_queue_name)
print('Consuming on {}'.format(input_queue_name))

# -----------------------------------------------------------------------------

#class TestImageProcessor(unittest.TestCase):
#    def test_processImage(self):
#        image = cv2.imread('test/bar.png')
#        findRects(image)
#        pass


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    channel.start_consuming()
