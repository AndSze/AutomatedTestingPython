from db import db

# ItemModel class is a piece of code that links SQLalchemy db with our code
class ItemModel(db.Model):                          # inherits from db.Model, which is db = SQLAlchemy()
    __tablename__ = 'items'                         # table name definition

    id = db.Column(db.Integer, primary_key=True)    # columns definition
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # store represents another table in db, so we have links between store_id in "items" table and "id" in "store" table
    # Postgres, MySQL will not let you delete store_id = 1 if it is used any element from user table uses it
    # SQLite allows for the above
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    # the above code lets Python now about the relationship in db = SQLAlchemy()
    # thanks to the above code, ItemModel will automatically have access StoreModel object

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SQLalchemy used to find an items

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
