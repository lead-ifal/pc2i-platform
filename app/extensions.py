"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mqtt import Mqtt

#bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
database = PyMongo()
cors = CORS()
mqtt = Mqtt(connect_async=True)
