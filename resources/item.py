
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")
        
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

        
    def post(self, name): # this function will have a JSON payload attached to it

        # error first-approach
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        
        #item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # Internal server error
            
        return item.json(), 201

        
    # overwrite items list with all of the elements except the one that has to be deleted
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {'message': 'Item deleted.'}

    
    def put(self, name): # this will have a JSON payload attached to it
        data = Item.parser.parse_args()

        # filter list of items to get specified item (None if not found)
        item = ItemModel.find_by_name(name)

        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
            # item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()
        
        return item.json()

            
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
