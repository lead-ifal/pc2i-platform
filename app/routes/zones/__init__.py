from flask import Blueprint

zones_routes = Blueprint('zones', __name__)

from flask import request
from app.controllers.global_controller import GlobalController
from app.models.zone import Zone
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from typing import Collection
from app import database

zones: Collection = database.zones

@zones_routes.route('/zone/new', methods = ['POST'])
def create():
  requiredParams = ['name', 'description', 'size']
  body = request.get_json()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  try:
    if includesParams:
      zone = Zone(**body)
      zoneData = zone.dict(exclude_none=True)

      zones.insert_one(zoneData)

      return GlobalController.generateResponse(HTTP_CREATED_CODE, SUCCESS_MESSAGE, zoneData)

    raise Exception()

  except:
    return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)
