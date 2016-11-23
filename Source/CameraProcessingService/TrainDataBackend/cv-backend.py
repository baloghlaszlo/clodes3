import flask
from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


# Connect to bigMongo
client = MongoClient('mongodb://clodes3:TopCPSKek@baprof.net/clodes3')
collection = client['clodes3']['images']

class Frame(Resource):
    def post(self):
        pass


@app.route('/frames/:frame_id', methods=['GET'])
def get_frame(frame_id):
    pass


@app.route('/')
@app.route('/label-rects')
@app.route('/label-frames')
@app.route('/frames/new')
@app.route('/frames/last')
@app.route('/stats')
def index():
    return flask.render_template('index.jinja2')

api.add_resource(Frame, '/frames')

if __name__ == '__main__':
    app.run(debug=True)
