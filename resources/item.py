from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    # Specify data which should be processed while parsing, other will be dissmissed
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type = float,
        required =True,
        # Required = True, means that the only specific data will be processed
        help = "This field cannot be left blank"
        )
    parser.add_argument(
        'store_id',
        type = int,
        required =True,
        # Required = True, means that the only specific data will be processed
        help = "Every item needs a store ID"
        )

    #Get an Item from DB
    @jwt_required()     # execute Authorisation header JWT()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':"item not found"}, 404

    #Post new item into DB
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':"An item already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return 500
        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':"Item deleted"}
        else:
            return {'message':"Item does not exist"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
