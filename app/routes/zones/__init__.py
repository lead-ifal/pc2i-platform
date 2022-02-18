from flask import Blueprint

zones_routes = Blueprint('zones', __name__)

from flask import request
from app.controllers.global_controller import GlobalController
from app.controllers.zone_controller import ZoneController
from app.models.zone import Zone
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE
from typing import Collection
from app import database

zones: Collection = database.zones

@zones_routes.route('/zone/new', methods = ['POST'])
def create():
  requiredParams = ['name', 'description', 'size']
  body = request.get_json()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  if includesParams:
    try:
      body['_id'] = ZoneController.buildZoneId(zones)
      zone = Zone(**body)
      zoneData = zone.dict(by_alias=True)

      zones.insert_one(zoneData)

      message = 'Zone de irrigação criada com sucesso'
      return GlobalController.generateResponse(HTTP_CREATED_CODE, message, zoneData)
    except:
      errorMessage = 'Não foi possível criar uma zona de irrigação com os dados informados'
      return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)
  
  errorMessage = 'Os parâmetros "name", "description" e "size" são obrigatórios'
  return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)
