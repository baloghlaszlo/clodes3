import json
import os
import ssl
import uuid

import pika
from bson import BSON
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import DuplicateKeyError

if 'FEATURES' in os.environ:
    features = os.environ['FEATURES'].split(':')

if 'VCAP_SERVICES' in os.environ:
    rabbitInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-rabbitmq'][0]
    rabbitCred = rabbitInfo["credentials"]
    mongoInfo = json.loads(os.environ['VCAP_SERVICES'])['compose-for-mongodb'][0]
    mongoCred = mongoInfo["credentials"]
else:
    rabbitCred = {'uri': 'amqp://localhost'}
    mongoCred = {'uri': 'localhost'}

# Connect to Mongo
client = MongoClient(mongoCred['uri'], ssl_cert_reqs=ssl.CERT_NONE)
collection = client['clodes3_frame_concentrator']['frames']
collection.create_index('id', unique=True)
collection.create_index('rects_pending.id')
collection.create_index('faces_found.id')

def dict_filter(d, keys):
    """From http://code.activestate.com/recipes/115417-subset-of-a-dictionary/#c2"""
    return dict((k, d[k]) for k in keys if k in d)


def on_new_image(ch, method_frame, header_frame, body):
    new_image = BSON.decode(body)
    print('Image {}: new image from {} (taken: {}, received: {})'.format(
        new_image['id'], new_image['camera_id'], new_image['camera_timestamp'], new_image['receive_timestamp']))

    document = dict_filter(new_image, ['id', 'camera_timestamp', 'camera_id', 'receive_timestamp'])
    document['features_pending'] = features
    document['rects_pending'] = []
    document['faces_found'] = []

    try:
        collection.insert(document)
        find_rects_new = dict_filter(new_image, ['id', 'image'])
        ch.basic_publish(routing_key='image.find_rects.new', exchange='amq.topic', body=BSON.encode(find_rects_new))
    except DuplicateKeyError:
        pass
    ch.basic_ack(delivery_tag=method_frame.delivery_tag)


IS_PIPELINE_COMPLETED_PROJECTION = {
    'features_pending': {'$slice': 1},
    'rects_pending': {'$slice': 1}
}

def is_pipeline_completed(updated):
    return updated is not None and len(updated['features_pending']) == 0 and len(updated['rects_pending']) == 0


def handle_pipeline_completed(ch, frame_id):
    document = collection.find_one({'id': frame_id})

    print('Image {}: done, {} faces found'.format(document['id'], len(document['faces_found'])))

    msg = dict_filter(document, ['id', 'camera_timestamp', 'camera_id', 'receive_timestamp'])
    msg['faces_found'] = list(map(lambda x: dict_filter(x, ['x', 'y', 'width', 'height', 'feature_name']),
                              document['faces_found']))
    ch.basic_publish(routing_key='image.faces.done', exchange='amq.topic', body=BSON.encode(msg))


def on_find_rects_done(ch, method_frame, header_frame, body):
    find_rects_done = BSON.decode(body)
    print('Image {}: feature {} found {} rects'.format(
        find_rects_done['id'], find_rects_done['feature_name'], len(find_rects_done['rects_found'])))

    rects_to_save = []  # Rects to save to MongoDB, metadata only.
    rects_to_send = []  # Rects to run the CNN processor on, id and payload only.
    for rect_found in find_rects_done['rects_found']:
        rect_id = str(uuid.uuid1())

        metadata = dict_filter(rect_found, ['x', 'y', 'width', 'height', 'feature_name'])
        metadata['id'] = rect_id
        rects_to_save.append(metadata)

        payload_data = {
            'id': rect_id,
            'feature_name': find_rects_done['feature_name'],
            'payload': rect_found['payload']
        }
        rects_to_send.append(payload_data)

    frame_id = find_rects_done['id']
    feature_name = find_rects_done['feature_name']
    updated = collection.find_one_and_update({
        'id': frame_id,
        'features_pending': feature_name
    }, {
        '$pull': {'features_pending': feature_name},
        '$push': {'rects_pending': {'$each': rects_to_save}}
    }, projection=IS_PIPELINE_COMPLETED_PROJECTION, return_document=ReturnDocument.AFTER)

    if is_pipeline_completed(updated):
        handle_pipeline_completed(ch, frame_id)
    elif updated is not None:  # Only send rects to CNN processor if the feature was pending (at-least-once).
        for msg in rects_to_send:
            ch.basic_publish(routing_key='rects.new.' + msg['feature_name'], exchange='amq.topic', body=BSON.encode(msg))

    ch.basic_ack(delivery_tag=method_frame.delivery_tag)


def on_rects_done(ch, method_frame, header_frame, body):
    rect_done = BSON.decode(body)

    matched_frame = collection.find_one({
        'rects_pending.id': rect_done['id']
    }, projection={
        'id': 1,
        'rects_pending.$': 1
    })

    if matched_frame is not None:
        frame_id = matched_frame['id']
        matched_rect = matched_frame['rects_pending'][0]
        update = {
            '$pull': {'rects_pending': {'id': matched_rect['id']}}
        }
        if rect_done['label'] == 1:
            update['$push'] = {'faces_found': matched_rect}
        updated = collection.find_one_and_update({
            'id': frame_id,
            'rects_pending.id': matched_rect['id']  # Also prepare for at-least-once delivery here.
        }, update, projection=IS_PIPELINE_COMPLETED_PROJECTION, return_document=ReturnDocument.AFTER)

        if is_pipeline_completed(updated):
            handle_pipeline_completed(ch, frame_id)

    ch.basic_ack(delivery_tag=method_frame.delivery_tag)


def subscribe_to_topic(ch, topic, callback):
    queue = "frame_concentrator.{}".format(topic)
    ch.queue_declare(queue=queue, arguments={'x-message-ttl': 60000})
    ch.queue_bind(exchange='amq.topic', queue=queue, routing_key=topic)
    ch.basic_consume(consumer_callback=callback, queue=queue)


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(url=rabbitCred['uri']))
channel = connection.channel()

subscribe_to_topic(channel, 'image.new', on_new_image)
subscribe_to_topic(channel, 'image.find_rects.done.*', on_find_rects_done)
subscribe_to_topic(channel, 'rects.classify.done.*', on_rects_done)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print('Starting to synchronously consume messages')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
