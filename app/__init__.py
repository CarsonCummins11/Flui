from flask import Flask
from pymongo import MongoClient
from flask_login import LoginManager
import os

client = MongoClient()
db = client['matcher']
app = Flask(__name__, static_url_path='/static')
login=LoginManager(app)
app.config['SECRET_KEY'] = os.urandom(20).hex()

from app import routes