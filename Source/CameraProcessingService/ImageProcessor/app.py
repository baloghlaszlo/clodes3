import unittest

import json
import os
import uuid

import cv2
import numpy as np

from bson import BSON
import pika

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}

if 'HAAR_CASCADE' in os.environ:
    cascadeName = os.environ['HAAR_CASCADE']
    cascadePath = 'cascade/{}.xml'.format(cascadeName)
    if not os.path.isfile(cascadePath):
        raise FileNotFoundError('Cascade {} definition xml is not found'.format(cascadeName))
else:
    raise EnvironmentError('Environmental variable HAAR_CASCADE is not defined')

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()
queue_name = 'image.find_rects.done.{}'.format(cascadeName)
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange='amq.topic', queue="image.new")

# -----------------------------------------------------------------------------

detector = cv2.CascadeClassifier(cascadePath)

def findRects(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)

    # cv2.imshow('test', equalized)
    # cv2.waitKey(0)

    rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1)
    print(len(rects))

    processedRects = []
    for (x, y, w, h) in rects:
        print((x, y, w, h))
        cropped = image[y:(y+64), x:(x+64)]
        (ret, croppedJpg) = cv2.imencode('.jpg', cropped)

        processedRect = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'payload': croppedJpg.tostring()
        }
        print(processedRect)
        processedRects.append(processedRect)

    return processedRects

def newImageCallback(channel, method, properties, body):
    decoded = BSON.decode(body)
    print(decoded)

    image = cv2.imdecode(np.frombuffer(bytes(decoded['picture'])), flags=cv2.IMREAD_COLOR)
    print(image)
    cv2.imshow('test', image)
    cv2.waitKey()
    rects = findRects(image)

    msg = {
        'id': body['id'],
        'feature_name': cascadeName,
        'rects_found': rects
    }

    channel.basic_publish(routing_key=queue_name, body=BSON.encode(msg))

pass

channel.basic_consume(newImageCallback, queue='image.new')
print('Consuming on {}'.format(queue_name))

# -----------------------------------------------------------------------------

class TestImageProcessor(unittest.TestCase):
    def test_processImage(self):
        image = cv2.imread('test/bar.png')
        findRects(image)
        pass


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    channel.start_consuming()
