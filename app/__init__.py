from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

pymongo_client = PyMongo(app)
database = pymongo_client.db

from .routes.users import users_routes as users_blueprint
app.register_blueprint(users_blueprint)