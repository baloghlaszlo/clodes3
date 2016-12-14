import os
import io

import time
import pika
import pika.exceptions
import json
import uuid

from bson import BSON
from werkzeug.datastructures import FileStorage
from flask import Flask, redirect
from flask_restful import Api, Resource, reqparse

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}

# Connect to RabbitMQ
#connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
#channel = connection.channel()

# -----------------------------------------------------------------------------

class Frame(Resource):
    def post(self):
        global connection, channel

        parser = reqparse.RequestParser()
        parser.add_argument('camera_id', required=True, type=int, location='form')
        parser.add_argument('camera_timestamp', required=True, type=int, location='form')
        parser.add_argument('image', required=True, type=FileStorage, location='files')
        args = parser.parse_args()

        image = args['image'].read()

        msg = {
            'id': str(uuid.uuid1()),
            'camera_id': args['camera_id'],
            'camera_timestamp': args['camera_timestamp'],
            'receive_timestamp': int(time.time()),
            'image': bytes(image),
        }

        print('Camera id: {}, camera timestamp: {}'.format(args['camera_id'], args['camera_timestamp']))

        connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
        channel = connection.channel()
        channel.basic_publish(routing_key='image.new', exchange='amq.topic', body=BSON.encode(msg))
        connection.close()

app = Flask('ImgProcGateway')
api = Api(app)

api.add_resource(Frame, '/api/frames')

if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        PORT = int(os.getenv('VCAP_APP_PORT'))
        HOST = str(os.getenv('VCAP_APP_HOST'))
    else:
        PORT = 8080
        HOST = '0.0.0.0'
    print('Starting flask service on {}:{}'.format(HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True)