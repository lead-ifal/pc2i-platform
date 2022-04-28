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

from .routes.zones import zones_routes as zones_blueprint
app.register_blueprint(zones_blueprint)

from .routes.cultures import cultures_routes as cultures_blueprint
app.register_blueprint(cultures_blueprint)
