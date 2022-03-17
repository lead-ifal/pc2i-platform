from flask import Blueprint

cultures_routes = Blueprint('cultures', __name__)

from flask import request
from bson import ObjectId
from datetime import datetime
from app.controllers.global_controller import GlobalController
from app.models.culture import Culture
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE
from typing import Collection
from app import database

cultures: Collection = database.cultures
zones: Collection = database.zones

@cultures_routes.route('/culture/new', methods = ['POST'])
def create():
  requiredParams = [
    "zone_id",
    "name",
    "type",
    "planting_date",
    "harvest_date",
    "ratio",
    "phase",
    "geographic_coordinates"
  ]
  body = request.get_json()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  if includesParams:
    try:
      body['planting_date'] = datetime.fromisoformat(body['planting_date'])
      body['harvest_date'] = datetime.fromisoformat(body['harvest_date'])
      body['geographic_coordinates'] = {
        'type': 'Point',
        'coordinates': body['geographic_coordinates']
      }

      culture = Culture(**body)
      zone_id = ObjectId(culture.zone_id)
      cultureData = culture.dict(exclude_none=True)
      zonesWithGivenId = zones.count({'_id': zone_id})
      zoneExists = zonesWithGivenId == 1

      if zoneExists:
        cultures.insert_one(cultureData)

        message = 'Cultura criada com sucesso'
        return GlobalController.generateResponse(HTTP_CREATED_CODE, message, cultureData)
      else:
        errorMessage = 'Não existe zona de irrigação com o ID informado'
        return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)

    except:
      errorMessage = 'Não foi possível criar uma cultura com os dados informados'
      return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)
  
  errorMessage = 'Os parâmetros "zone_id", "name", "type", "planting_date", "harvest_date", "ratio", "phase", "geographic_coordinates" são obrigatórios'
  return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)
