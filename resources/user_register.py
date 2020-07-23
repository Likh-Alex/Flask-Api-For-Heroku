import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()               # Specify data which should be processed while parsing, other will be dissmissed
    parser.add_argument('username',
        type = str,
        required=True,
        help = "This field cannot be blank."
    )
    parser.add_argument('password',
        type = str,
        required=True,
        help = "This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()                                 # assign parsed request to variable data

        if UserModel.find_by_username(data['username']):                                 # call to User class func, check for username, if it exists:
            return {'message':'User with that username already exists'}, 400    #return message and 400
        # if doesn't exists do the following
        user = UserModel(**data)
        user.save_to_db()

        return {"message":"User created successfully."}, 201
