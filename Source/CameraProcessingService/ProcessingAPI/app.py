import os
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
channel.queue_bind(exchange='amq.topic', queue="image.new")

class Frame(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timestamp', type=int)
        parser.add_argument('picture', required=True, type=FileStorage, location='files')
        args = parser.parse_args()

        msg = {
            'id': str(uuid.uuid1()),
            'timestamp': args['timestamp'],
            'picture': args['picture'].read()
        }
        channel.basic_publish(routing_key='image.new', body=BSON.encode(msg))


app = Flask('ImgProcGateway')
api = Api(app)

api.add_resource(Frame, '/api/frames')

if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        PORT = int(os.getenv('VCAP_APP_PORT'))
        HOST = str(os.getenv('VCAP_APP_HOST'))
    else:
        PORT = 8080
        HOST = 'localhost'
    print('Starting flask service on {}:{}'.format(HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True)