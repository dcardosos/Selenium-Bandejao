from flask import Flask
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False) # max character / has to have some information
    likes = db.Column(db.Integer, nullable = False)
    views = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return "Video(name = {}, views = {}. likes = {})".format(name, views, likes)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help = "Name of the video")
video_update_args.add_argument("likes", type=int, help = "Likes of the video")
video_update_args.add_argument("views", type=int, help = "Views of the video")


video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name", type=str, help = "Name of the video", required = True)
video_post_args.add_argument("likes", type=int, help = "Likes of the video", required = True)
video_post_args.add_argument("views", type=int, help = "Views of the video", required = True)

# serialize objects
resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields) # when we return, take the result value and serialize it with resource_fields
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first() #all()
        if not result:
            abort(404, message="Coult not find video with that id")
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409, message="Video id taken...")

        video = VideoModel(id = video_id, name = args['name'], likes = args['likes'], views = args['views'])
        db.session.add(video)
        db.session.commit()
        # db.session.close()
        return video, 201 # created

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="video doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']

        db.session.commit()

        return result

    # def delete(self, video_id):
    #     del videos[video_id]
    #     return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)