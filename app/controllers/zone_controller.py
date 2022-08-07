import requests
from bson import ObjectId

from app.models.schedule_irrigation import ScheduleIrrigation
from config import Config
from flask import jsonify, request
from typing import Collection
from app.extensions import database, mqtt
from app.controllers.global_controller import GlobalController
from app.models.irrigation_zone import IrrigationZone
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE, HTTP_NOT_FOUND,HTTP_SERVER_ERROR
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE, ZONE_NOT_FOUND,INTERNAL_SERVER_ERROR
from app.constants.required_params import required_params


irrigation_zones: Collection = database.db.irrigation_zones
scheduled_irrigations: Collection = database.db.scheduled_irrigations
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

  def schedule_irrigation():
    body = request.get_json()
    params = required_params['irrigation_zones']['schedule']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:
        scheduling = ScheduleIrrigation(**body)
        schedule_irrigation_data = scheduling.dict(exclude_none=True)

        scheduled_irrigations.insert_one(schedule_irrigation_data)

        return GlobalController.generate_response(
          HTTP_CREATED_CODE,
          SUCCESS_MESSAGE,
          schedule_irrigation_data
        )

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)



  def show(zone_id):
    try:
      irrigation_zone = None
      if (len(zone_id)) == 24:
        irrigation_zone = irrigation_zones.find_one({ '_id': ObjectId(zone_id) })
      if irrigation_zone != None:
        return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_zone)
      return GlobalController.generate_response(HTTP_NOT_FOUND, ZONE_NOT_FOUND)

      raise Exception()
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR,INTERNAL_SERVER_ERROR )

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