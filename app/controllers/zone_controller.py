import requests
from bson import ObjectId
from config import Config
from flask import jsonify, request
from typing import Collection
from app.extensions import database, mqtt
from app.controllers.global_controller import GlobalController
from app.models.irrigation_zone import IrrigationZone
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from app.constants.required_params import required_params

irrigation_zones: Collection = database.db.irrigation_zones
mqtt: mqtt


class ZoneController:
  irrigation_status = False


  def create():
    print(request)
    body = request.get_json()
    params = required_params['irrigation_zones']['create']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:
        irrigation_zone = IrrigationZone(**body)
        irrigation_zone_data = irrigation_zone.dict(exclude_none=True)

        irrigation_zones.insert_one(irrigation_zone_data)

        return GlobalController.generate_response(
          HTTP_CREATED_CODE,
          SUCCESS_MESSAGE,
          irrigation_zone_data
        )

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

  def show(zone_id):
    irrigation_zone_list = irrigation_zones.findone({ '_id': ObjectId(zone_id) })
    data = []

    for irrigation_zone in irrigation_zone_list:
      data.append(irrigation_zone)

    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)


  def list(user_id):
    irrigation_zone_list = irrigation_zones.find({ 'user_id': user_id })
    data = []

    for irrigation_zone in irrigation_zone_list:
      data.append(irrigation_zone)

    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)


  def toggle_irrigation(zone_id=None):
    ZoneController.irrigation_status = not ZoneController.irrigation_status
    print(ZoneController.irrigation_status)
    print(Config.PC2I_ESP_ADDRESS)
    requests.get(Config.PC2I_ESP_ADDRESS+'/irrigation/'+str(ZoneController.irrigation_status))