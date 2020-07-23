from models.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

"""
Identity function takes in a payload
Payload is the contents of the JWT Token
Extract the user ID from that payload return userID
to the find_by_id() of User class
"""

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
