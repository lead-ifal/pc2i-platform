from distutils.util import strtobool
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

class Config:
  DEBUG = True
  DEV_MODE = True if strtobool(os.getenv('DEV_MODE')) == 1 else False
  MONGO_URI = os.getenv('MONGO_URI')
  MQTT_BROKER_URL = os.getenv('BROKER_URL')
  MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT'))
  PC2I_ESP_ADDRESS = os.getenv('PC2I_ESP_ADDRESS')
