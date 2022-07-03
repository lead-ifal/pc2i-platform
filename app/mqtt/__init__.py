from flask_mqtt import Mqtt
from app import app

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
  mqtt.subscribe('temperature')
  mqtt.subscribe('humidity')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
  data = dict(
    topic=message.topic,
    payload=message.payload.decode()
  )

  print(data)
