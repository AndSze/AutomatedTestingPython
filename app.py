import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True
# if 'DATABASE_URL' not set, get() will use the default value: 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose123'
api = Api(app)  # create API part of flask RESTful

jwt = JWT(app, authenticate, identity) # /auth

# added more endpoints used for requesting the below resources
# ItemList and StoreList are auxiliary classes that return a dict with all items/stores
# endpoint - address from a client's request
# adds an item to our endpoint: '/item/<string:name>', adds endpoint handling for GET, POST, PUT
api.add_resource(Item, '/item/<string:name>')   # adds a resource that goes into our Item resource
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

@app.errorhandler(JWTError) # endpoint error handler in Flask, every time an error occurs, this piece of code is called
def auth_error_handler(err):
    return jsonify({'message': "Could not authorize. Did you include a valid Authorization header?"}), 401

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request # decorator that will be run before first request to db
        def create_tables():      # SQLAlchemy is used to create database tables for us
            db.create_all()

    app.run(port=5000)
