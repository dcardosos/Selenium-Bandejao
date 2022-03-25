from flask import Flask
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class CardapioModel(db.Model):
    id =  db.Column(db.String(20), primary_key=True)
    basico = db.Column(db.String(100))
    mistura = db.Column(db.String(100)) # max character / has to have some information
    pvt = db.Column(db.String(100))
    salada1 =db.Column(db.String(100))
    salada2 = db.Column(db.String(100))
    fruta = db.Column(db.String(100))
    complemento = db.Column(db.String(100))
    
    def __repr__(self):
        return "Cardapio(basico = {}, mistura = {}, pvt = {}, salada1 = {}, salada2 = {}, fruta = {}, complemento = {})".format(basico, mistura, pvt, salada1, salada2, fruta, complemento)

db.creat_all()

# video_update_args = reqparse.RequestParser()
# video_update_args.add_argument("name", type=str, help = "Name of the video")
# video_update_args.add_argument("likes", type=int, help = "Likes of the video")
# video_update_args.add_argument("views", type=int, help = "Views of the video")


cardapio_post_args = reqparse.RequestParser()
cardapio_post_args.add_argument("basico", type=str)
cardapio_post_args.add_argument("mistura", type=str)
cardapio_post_args.add_argument("pvt", type=str)
cardapio_post_args.add_argument("salada1", type=str)
cardapio_post_args.add_argument("salada2", type=str)
cardapio_post_args.add_argument("fruta", type=str)
cardapio_post_args.add_argument("complemento", type=str)

# serialize objects
resource_fields = {
    'id': fields.String,
    'basico': fields.String,  
    'mistura': fields.String, 
    'pvt': fields.String, 
    'salada1': fields.String, 
    'salada2': fields.String, 
    'fruta': fields.String, 
    'complemento': fields.String
}

class Cardapio(Resource):
    @marshal_with(resource_fields) # when we return, take the result value and serialize it with resource_fields
    def get(self, cardapio_id):
        result = CardapioModel.query.filter_by(id = cardapio_id).first() #all()
        if not result:
            abort(404, message="Coult not find cardapio with that id")
        return result

    @marshal_with(resource_fields)
    def post(self, cardapio_id):
        args = cardapio_post_args.parse_args()
        result = CardapioModel.query.filter_by(id = cardapio_id).first()
        if result:
            abort(409, message="Cardapio id taken...")

        cardapio = CardapioModel(
            id = cardapio_id, 
            basico = args['basico'], 
            mistura = args['mistura'],
            pvt = args['pvt'], 
            salada1 = args['salada1'],
            salada2 = args['salada2'],
            fruta = args['fruta'],
            complemento = args['complemento'])

        db.session.add(cardapio)
        db.session.commit()
        # db.session.close()
        return cardapio, 201 # created

    # @marshal_with(resource_fields)
    # def put(self, video_id):
    #     args = video_update_args.parse_args()
    #     result = VideoModel.query.filter_by(id = video_id).first()
    #     if not result:
    #         abort(404, message="video doesn't exist, cannot update")

    #     if args['name']:
    #         result.name = args['name']
    #     if args["views"]:
    #         result.views = args['views']
    #     if args["likes"]:
    #         result.likes = args['likes']

    #     db.session.commit()

    #     return result

    # def delete(self, video_id):
    #     del videos[video_id]
    #     return '', 204

api.add_resource(Cardapio, "/cardapio/<string:cardapio_id>")

if __name__ == "__main__":
    app.run(debug=True)