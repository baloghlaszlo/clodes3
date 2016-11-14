import pika

features = [
    "haarcascade_frontalface_alt",
    "haarcascade_frontalface_alt2",
    "haarcascade_frontalface_alt_tree",
    "haarcascade_frontalface_default",
    "haarcascade_profileface"
]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='imgProcNodeFanout', type='fanout', durable=True)

channel.queue_declare("newImage")

for feature in features:
    queue = "imgProcNodeProcess_{}".format(feature)
    channel.queue_declare(queue=queue)
    channel.queue_bind(queue=queue, exchange="imgProcNodeFanout")

channel.queue_declare("cnnNodeProcess")
channel.queue_declare("cnnNodeDone")

channel.queue_declare("aggregatorNodeProcess")
channel.queue_declare("aggregatorNodeDone")

input("Press Enter to continue...")