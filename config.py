import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

class Config:
  DEBUG = True
  MONGO_URI = os.getenv('MONGO_URI')
  MQTT_BROKER_URL = os.getenv('BROKER_URL')
  MQTT_BROKER_PORT = 80
  
