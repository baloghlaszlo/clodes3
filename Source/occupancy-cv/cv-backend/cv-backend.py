import flask
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


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
