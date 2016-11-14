import pika
from bson import BSON
from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask('ImgProcGateway')
api = Api(app)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_bind(exchange='ImgProcNodeFanout', queue="ImgProcNode", type=)

class Frame(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timestamp', type=int)
        parser.add_argument('picture', required=True, type=FileStorage, location='files')



        args = parser.parse_args()
        print(args)

api.add_resource(Frame, '/api/frames')

if __name__ == '__main__':
    app.run(debug=True)