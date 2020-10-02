from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):  # item is a flask RESTful resource
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    # added parser for StoreModel
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")


    # it will be called every time client makes HTTP GET request on '/item/<string:name>' endpoint
    @jwt_required() # decorator -> checks before each call of get() method if the auth header was included within jwt that we call when we authenticate (call '/auth' endpoint)
    def get(self, name):
        item = ItemModel.find_by_name(name)  # searches for an item in database
        if item:
            return item.json()  # returns json representation of an item
        return {'message': 'Item not found'}, 404

    # handles client's HTTP POST requests
    def post(self, name):  # creates an item if it does not exist
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()  # looks at item create request and extracts all arguments from parser.add_argument

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message': 'Item to be deleted does not exist'}
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
