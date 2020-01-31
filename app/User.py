from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import db,login

@login.user_loader
def load_user(username):
    u = db['advertisers'].find_one({'user':username})
    if not u:
        u = db['influencers'].find_one({'user':username})
    if not u:
        return None
    return User(username=u['user'])
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

    def get_id(self):
        return self.username
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    @staticmethod
    def check_password(hash,pw):
        return check_password_hash(hash,pw)
    