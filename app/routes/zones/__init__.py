from flask import Blueprint

zones_routes = Blueprint('zones', __name__)

from flask import request
from app.controllers.global_controller import GlobalController
from app.models.zone import Zone
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
      zone = Zone(**body)
      zones.insert_one(zone.dict())

      message = 'Zone de irrigação criada com sucesso'
      return GlobalController.generateResponse(200, message, body)
    except:
      errorMessage = 'Não foi possível criar uma zona de irrigação com os dados informados'
      return GlobalController.generateResponse(400, errorMessage)
  
  errorMessage = 'Os parâmetros "name", "description" e "size" são obrigatórios'
  return GlobalController.generateResponse(400, errorMessage)