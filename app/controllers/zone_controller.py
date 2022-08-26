import requests
from bson import ObjectId
import threading
import time
from datetime import datetime
from app.models.schedule_irrigation import ScheduleIrrigation
from config import Config
from flask import request
from typing import Collection
from app.extensions import database, mqtt
from app.middlewares.has_token import has_token
from app.controllers.global_controller import GlobalController
from app.models.irrigation_zone import IrrigationZone
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE, HTTP_NOT_FOUND_CODE, \
  HTTP_SERVER_ERROR_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE, ZONE_NOT_FOUND_MESSAGE, \
  INTERNAL_SERVER_ERROR_MESSAGE
from app.constants.required_params import required_params

irrigation_zones: Collection = database.db.irrigation_zones
scheduled_irrigations: Collection = database.db.scheduled_irrigations
mqtt: mqtt
loping = True

class ZoneController:
  irrigation_status = False

  @has_token
  def create():
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

  @has_token
  def delete():
    body = request.get_json()
    params = required_params['irrigation_zones']['delete']
    includes_params = GlobalController.includes_all_required_params(params, body)
    try:
      if includes_params:
        irrigation_zone_exists = False
        id = body["irrigation_zone_id"]
        valid_id = GlobalController.is_valid_mongodb_id(id)
        if valid_id:
          irrigation_zone_exists = irrigation_zones.count({'_id': ObjectId(id)}) == 1

        if irrigation_zone_exists:
          irrigation_zones.delete_one({'_id': ObjectId(id)})

          return GlobalController.generate_response(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            id
          )
        else:
          return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, ZONE_NOT_FOUND_MESSAGE)

      raise Exception()
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE)

  @has_token
  def edit():
    body = request.get_json()
    params = required_params['irrigation_zones']['update']
    includes_params = GlobalController.includes_all_required_params(params, body)
    try:
      if includes_params:
        irrigation_zone_exists = False
        id = body["irrigation_zone_id"]
        valid_id = GlobalController.is_valid_mongodb_id(id)
        if valid_id:
          irrigation_zone_exists = irrigation_zones.count({'_id': ObjectId(id)}) == 1

        if irrigation_zone_exists:
          body.pop("irrigation_zone_id")
          irrigation_zone = IrrigationZone(**body)
          irrigation_zone_data = irrigation_zone.dict(exclude_none=True)
          irrigation_zones.update_one({'_id': ObjectId(id)}, {"$set": irrigation_zone_data})

          return GlobalController.generate_response(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            id
          )
        else:
          return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, ZONE_NOT_FOUND_MESSAGE)

      raise Exception()
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE)

  @has_token
  def edit_schedule():
    body = request.get_json()
    params = required_params['irrigation_zones']['schedule']
    includes_params = GlobalController.includes_all_required_params(params, body)
    try:
      if includes_params:
        schedule_exists = False
        id = body["schedule_id"]
        valid_id = GlobalController.is_valid_mongodb_id(id)
        if valid_id:
          schedule_exists = scheduled_irrigations.count({'_id': ObjectId(id)}) == 1

        if schedule_exists:
          body.pop("schedule_id")
          scheduling = ScheduleIrrigation(**body)
          schedule_irrigation_data = scheduling.dict(exclude_none=True)
          scheduled_irrigations.update_one({'_id': ObjectId(id)}, {"$set": schedule_irrigation_data})

          return GlobalController.generate_response(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            id
          )
        else:
          return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, ZONE_NOT_FOUND_MESSAGE)

      raise Exception()
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE)

  @has_token
  def delete_schedule():
    body = request.get_json()
    params = required_params['irrigation_zones']['delete_schedule']
    includes_params = GlobalController.includes_all_required_params(params, body)
    try:
      if includes_params:
        schedule_exists = False
        id = body["schedule_id"]
        valid_id = GlobalController.is_valid_mongodb_id(id)
        if valid_id:
          schedule_exists = scheduled_irrigations.count({'_id': ObjectId(id)}) == 1

        if schedule_exists:
          scheduled_irrigations.delete_one({'_id': ObjectId(id)})

          return GlobalController.generate_response(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            id
          )
        else:
          return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, ZONE_NOT_FOUND_MESSAGE)

      raise Exception()
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE)


  @has_token
  def schedule_irrigation():
    body = request.get_json()
    params = required_params['irrigation_zones']['schedule']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:
        scheduling = ScheduleIrrigation(**body)
        schedule_irrigation_data = scheduling.dict(exclude_none=True)

        scheduled_irrigations.insert_one(schedule_irrigation_data)

        loping = False
        t.start()

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
      valid_id = GlobalController.is_valid_mongodb_id(zone_id)
      if valid_id:
        irrigation_zone = irrigation_zones.find_one({'_id': ObjectId(zone_id)})
        if irrigation_zone != None:
          return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_zone)
      return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, ZONE_NOT_FOUND_MESSAGE)
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE)


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

  def verify_schedule():

    while loping == True:
      data = []
      hour_to_seconds = 3600
      minutes_to_seconds = 60
      shorter_time = 86400
      current_time = datetime.now().time()
      current_time = current_time.second + current_time.minute * minutes_to_seconds + current_time.hour * hour_to_seconds
      day = datetime.today().weekday()
      schedule_list = scheduled_irrigations.find({})
      for schedule in schedule_list:
        data.append(schedule)
      for schedule in data:
        if day in schedule["days"]:
          if schedule["moment_of_activation"] < shorter_time:
            shorter_time = schedule["moment_of_activation"]
      wait = shorter_time - current_time
      nex_irrigation = scheduled_irrigations.find_one({'moment_of_activation': shorter_time})
      time.sleep(wait)
      ZoneController.toggle_irrigation(nex_irrigation["irrigation_zone_id"])


t = threading.Thread(target=ZoneController.verify_schedule)
t.start()
