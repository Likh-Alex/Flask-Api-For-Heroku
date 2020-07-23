from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_register import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)           #Creating an instance of Flask class with name(name is equal to __main__ as it runs itself and not imported)

app.secret_key = 'sasha'       #Anything that requires encryption (for safe-keeping against tampering by attackers)
                               #requires the secret key to be set. For just Flask itself, that 'anything' is the Session object,#
                               #but other extensions can make use of the same secret.
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWT(app, authenticate, identity)  # /authorization decorator, passes the parameters to security.py for processing

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)
