
from db import db


class ItemModel(db.Model):
    # specify talbename
    __tablename__ = 'items'

    # specify columns ==> this adds columns to the db
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    #                stores=table name, .id=column name in table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    
    def __init__(self, name, price, store_id):
        #self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        # this returns an ItemModel object with a self.name and self.price
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    # use this method for both insert and update
    def save_to_db(self):
        #SQlAlchemy can translate from object to row
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
