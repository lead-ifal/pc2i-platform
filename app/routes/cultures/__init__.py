from flask import Blueprint

cultures_routes = Blueprint('cultures', __name__)

from flask import request
from bson import ObjectId
from datetime import datetime
from app.controllers.global_controller import GlobalController
from app.models.culture import Culture
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from typing import Collection
from app import database

cultures: Collection = database.cultures
zones: Collection = database.zones

@cultures_routes.route('/culture/new', methods = ['POST'])
def create():
  requiredParams = ["zone_id", "name", "type", "planting_date", "harvest_date", "ratio", "phase", "geographic_coordinates"]
  body = request.get_json()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  try:
    if includesParams:
      body['planting_date'] = datetime.fromisoformat(body['planting_date'])
      body['harvest_date'] = datetime.fromisoformat(body['harvest_date'])
      body['geographic_coordinates'] = {
        'type': 'Point',
        'coordinates': body['geographic_coordinates']
      }

      culture = Culture(**body)
      zone_id = ObjectId(culture.zone_id)
      cultureData = culture.dict(exclude_none=True)
      zonesWithGivenId = zones.count({ '_id': zone_id })
      zoneExists = zonesWithGivenId == 1

      if zoneExists:
        cultures.insert_one(cultureData)

        return GlobalController.generateResponse(HTTP_CREATED_CODE, SUCCESS_MESSAGE, cultureData)

    raise Exception()

  except:
    return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)
