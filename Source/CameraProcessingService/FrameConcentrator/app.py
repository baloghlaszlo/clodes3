import os
import pika
import json
from pymongo import MongoClient

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
    mongoInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-mongodb'][0]
    mongoCred = mongoInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}
    mongoCred = {'uri': 'localhost'}

# Connect to bigMongo
client = MongoClient('mongodb://clodes3:TopCPSKek@baprof.net/clodes3')
collection = client['clodes3']['images']

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()
channel.queue_declare(queue='image.new', durable=True)
channel.queue_bind(exchange='amq.topic', queue="image.new")

# -----------------------------------------------------------------------------

# CODE GOES HERE

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        # Service is running in clud
        pass
    else:
        # Service is running locally
        pass