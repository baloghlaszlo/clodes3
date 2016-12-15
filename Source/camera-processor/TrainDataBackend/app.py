import os

import flask
from flask import Flask, abort, Response
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
api = Api(app)

# Connect to bigMongo
client = MongoClient('mongodb://clodes3:TopCPSKek@baprof.net/clodes3')
frames_collection = client['clodes3']['frames']
rects_collection = client['clodes3']['rects']


def get_random_unlabeled(collection):
    random = collection.aggregate([
        {'$match': {'label': {'$exists': False}}},
        {'$sample': {'size': 1}}
    ])
    for doc in random:
        return doc
    return None


def post_label(collection, item_id):
    parser = reqparse.RequestParser()
    parser.add_argument('label', required=True, type=int, location='json')
    args = parser.parse_args()
    collection.update({
        'id': item_id
    }, {
        '$set': {'label': args['label']}
    })


class Frame(Resource):
    def get(self):
        frame = get_random_unlabeled(frames_collection)
        if frame is None:
            abort(404, "There are no unlabeled frames.")
        return {
            'src': '/api/frames/{}.jpg'.format(frame['id']),
            'labels': {
                'uri': '/api/frames/{}/labels'.format(frame['id']),
                'type': 'count'
            }
        }


class FrameLabel(Resource):
    def post(self, frame_id):
        post_label(frames_collection, frame_id)



class Rect(Resource):
    def get(self):
        frame = get_random_unlabeled(rects_collection)
        if frame is None:
            abort(404, "There are no unlabeled rects.")
        return {
            'src': '/api/rects/{}.jpg'.format(frame['id']),
            'labels': {
                'uri': '/api/rects/{}/labels'.format(frame['id']),
                'type': 'face'
            }
        }


class RectLabel(Resource):
    def post(self, rect_id):
        post_label(rects_collection, rect_id)


api.add_resource(Frame, '/api/frames')
api.add_resource(FrameLabel, '/api/frames/<frame_id>/labels')
api.add_resource(Rect, '/api/rects')
api.add_resource(RectLabel, '/api/rects/<rect_id>/labels')


@app.route('/api/frames/<frame_id>.jpg', methods=['GET'])
def get_frame(frame_id):
    frame = frames_collection.find_one({'id': frame_id})
    if frame is None or 'image' not in frame:
        abort(404)
    return Response(frame['image'], mimetype='image/jpeg')


@app.route('/api/rects/<rect_id>.jpg', methods=['GET'])
def get_rect(rect_id):
    rect = rects_collection.find_one({'id': rect_id})
    if rect is None or 'payload' not in rect:
        abort(404)
    return Response(rect['payload'], mimetype='image/jpeg')


@app.route('/')
@app.route('/label-rects')
@app.route('/label-frames')
def index():
    return flask.render_template('index.jinja2')


if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        PORT = int(os.getenv('VCAP_APP_PORT'))
        HOST = str(os.getenv('VCAP_APP_HOST'))
    else:
        PORT = 8082
        HOST = '0.0.0.0'
    print('Starting flask service on {}:{}'.format(HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True)
