#User Class
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import db,login

#db = the database of users that uses mongodb

@login.user_loader
def load_user(username): #returns a user object if the username is present
    u = db['advertisers'].find_one({'user':username}) #Set to advertiser if an advertiser exists
    if not u:
        u = db['influencers'].find_one({'user':username}) #Set to an influencer if an influencer exists
    if not u:
        return None
    return User(username=u['user'])

#User class
class User:
    def __init__(self,username):
        self.username=username
    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self): #Are we going to have seperate ID's and usernames?
        return self.username
    def set_password(self,password):
        self.password_hash=generate_password_hash(password) #sets the password of the user with a hash
    @staticmethod
    def check_password(hash,pw):
        return check_password_hash(hash,pw) #checks if the password is correct using the hash
    