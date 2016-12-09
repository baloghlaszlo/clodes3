import json
import os

import cv2
import numpy as np
import pika
from bson import BSON
from bson import Int64

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}

if 'HAAR_CASCADE' in os.environ:
    cascade_name = os.environ['HAAR_CASCADE']
    cascade_path = 'cascade/{}.xml'.format(cascade_name)
    if not os.path.isfile(cascade_path):
        raise FileNotFoundError('Cascade {} definition xml is not found'.format(cascade_name))
else:
    raise EnvironmentError('Environmental variable HAAR_CASCADE is not defined')

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()
input_topic_name = 'image.find_rects.new'
input_queue_name = 'image_processor.{}.{}'.format(input_topic_name, cascade_name)
channel.queue_declare(queue=input_queue_name, arguments={'x-message-ttl': 60000})
channel.queue_bind(exchange='amq.topic', queue=input_queue_name, routing_key=input_topic_name)

output_topic_name = 'image.find_rects.done.{}'.format(cascade_name)

# -----------------------------------------------------------------------------

detector = cv2.CascadeClassifier(cascade_path)


def findRects(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)

    rects = detector.detectMultiScale(equalized, scaleFactor=1.1, minNeighbors=1)
    processedRects = []
    for (x, y, w, h) in rects:
        cropped = image[y:(y+h), x:(x+w)]
        longest_side = max(w, h)
        mat = np.zeros((2, 3), np.float32)
        max_size = 64
        scale = max_size / longest_side
        mat[0, 0] = mat[1, 1] = scale
        mat[0, 2] = (max_size - w * scale) / 2
        mat[1, 2] = (max_size - h * scale) / 2
        resized = cv2.warpAffine(cropped, mat, (max_size, max_size))
        # print(cropped.shape, resized.shape)
        # cv2.imshow("", resized)
        # cv2.waitKey(0)

        (ret, croppedJpg) = cv2.imencode('.jpg', cropped)

        processedRect = {
            'x': Int64(x),
            'y': Int64(y),
            'width': Int64(w),
            'height': Int64(h),
            'payload': croppedJpg.tobytes()
        }
        processedRects.append(processedRect)
    return processedRects


def newImageCallback(channel, method, properties, body):
    decoded = BSON.decode(body)

    image = cv2.imdecode(np.fromstring(decoded['image'], dtype=np.uint8), flags=cv2.IMREAD_COLOR)
    rects = findRects(image)
    print("Frame id {} processed, {} rects found".format(decoded['id'], len(rects)))

    msg = {
        'id': decoded['id'],
        'feature_name': cascade_name,
        'rects_found': rects
    }
    channel.basic_publish(routing_key=output_topic_name, exchange='amq.topic', body=BSON.encode(msg))
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
