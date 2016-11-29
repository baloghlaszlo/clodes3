import os
import io

import time
import pika
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
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()
channel.queue_declare(queue='image.new', durable=True)

# -----------------------------------------------------------------------------

class Frame(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('camera_id', type=int)
        parser.add_argument('camera_timestamp', type=int)
        parser.add_argument('picture', required=True, type=FileStorage, location='files')
        args = parser.parse_args()

        args['picture'].read()

        msg = {
            'id': str(uuid.uuid1()),
            'camera_id': args['camera_id'],
            'camera_timestamp': args['camera_timestamp'],
            'picture': io.BytesIO(args['picture'].read()),
            'receive_timestamp': int(time.time())
        }
        #print(msg)
        channel.basic_publish(routing_key='image.new', exchange='amq.topic', body=BSON.encode(msg))


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