from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

pymongo_client = PyMongo(app)
database = pymongo_client.db

from .routes.users import users_bp
from .routes.irrigation_zones import irrigation_zones_bp
from .routes.cultures import cultures_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(irrigation_zones_bp, url_prefix='/irrigation-zones')
app.register_blueprint(cultures_bp, url_prefix='/cultures')
