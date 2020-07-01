
from werkzeug.security import safe_str_cmp
from models.user import UserModel


# function to authenticate a user
def authenticate(username, password):
    # find user by username
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# function to identify a user
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

