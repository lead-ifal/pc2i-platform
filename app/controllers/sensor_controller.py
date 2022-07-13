import json
import bcrypt
from flask import jsonify, request
from typing import Collection
from app.extensions import database, mqtt
from app.models.sensor import Sensor
from app.controllers.global_controller import GlobalController
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from app.constants.required_params import required_params
from app.models.sensor_reading import SensorReading

sensors: Collection = database.db.sensors
sensors_readings: Collection = database.db.sensors_readings

class SensorController():

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

  def list():
    sensors_list = sensors.find()
    data = []

    for sensor in sensors_list:
      dictionary = {
        "id": str(sensor['_id']),
        "culture_id": sensor['culture_id'],
        "name": sensor['name'],
        "type": sensor['type'],
      }
      data.append(json.dumps(dictionary))

    print(data)
    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)

  @mqtt.on_message()
  def handle_messages(client, userdata, message):
    print(client)
    print(message)
    """body = request.get_json()
    sensor_reading = SensorReading(**body)
    result = sensors_readings.insert_one(sensor_reading.dict(exclude_none=True))
    sensor_reading_data = sensor_reading.dict(exclude_none=True)
    sensor_reading_data['_id'] = result.inserted_id

    if(sensor_reading_data['_id']):
      return GlobalController.generate_response(
        HTTP_CREATED_CODE,
        SUCCESS_MESSAGE,
        sensor_reading_data
      )

    raise Exception()"""