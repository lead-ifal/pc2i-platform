import json
from flask import request
from typing import Collection
from app.extensions import database, mqtt
from app.middlewares.has_token import has_token
from app.models.sensor import Sensor
from app.controllers.global_controller import GlobalController
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE,HTTP_SERVER_ERROR_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from app.constants.required_params import required_params
from app.models.sensor_reading import SensorReading

sensors: Collection = database.db.sensors
sensors_readings: Collection = database.db.sensors_readings

class SensorController():
  @has_token
  def create():
    body = request.get_json()
    params = required_params['sensors']['create']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:

        sensor = Sensor(**body)
        result = sensors.insert_one(sensor.dict(exclude_none=True))
        sensor_data = sensor.dict(exclude_none=True)
        sensor_data['_id'] = result.inserted_id

        return GlobalController.generate_response(
          HTTP_CREATED_CODE,
          SUCCESS_MESSAGE,
          sensor_data
        )

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

  def list(irrigation_zone_id):

    try:
      sensors_zone_list = sensors.find({ 'irrigation_zone_id' : irrigation_zone_id})
      data = []
      for sensor in sensors_zone_list: 
        data.append(sensor)

      return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)
    except: 
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, ERROR_MESSAGE)

  @has_token
  def publish(sensor_id, value):
    topic = 'pc2i/'+sensor_id
    mqtt.subscribe(topic)
    publish_result = mqtt.publish(topic, value)
    print("teste")
    print(publish_result)
    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, "publish_result")

  @mqtt.on_message()
  def handle_messages(client, userdata, message):
    body = {
        "sensor_id": message.topic.replace('pc2i/', ''),
        "value": message.payload.decode(),
    }
    print(body)
    sensor_reading = SensorReading(**body)
    print(sensor_reading)
    result = sensors_readings.insert_one(sensor_reading.dict(exclude_none=True))
    sensor_reading_data = sensor_reading.dict(exclude_none=True)
    sensor_reading_data['_id'] = result.inserted_id

    if(sensor_reading_data['_id']):
      return GlobalController.generate_response(
        HTTP_CREATED_CODE,
        SUCCESS_MESSAGE,
        sensor_reading_data
      )

    raise Exception()