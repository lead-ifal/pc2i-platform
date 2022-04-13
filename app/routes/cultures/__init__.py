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
from app import database, pymongo_client

cultures: Collection = database.cultures
zones: Collection = database.zones

@cultures_routes.route('/culture/new', methods = ['POST'])
def create():
  required_params = ["zone_id", "name", "type", "planting_date", "harvest_date", "ratio", "phase", "geographic_coordinates", "image"]
  body = { **request.form.to_dict(), **request.files.to_dict() }

  includes_params = GlobalController.includesAllRequiredParams(required_params, body)

  try:
    if includes_params:
      body['planting_date'] = datetime.fromisoformat(body['planting_date'])
      body['harvest_date'] = datetime.fromisoformat(body['harvest_date'])
      body['geographic_coordinates'] = {
        'type': 'Point',
        'coordinates': body['geographic_coordinates']
      }

      culture = Culture(**body)
      zone_id = ObjectId(culture.zone_id)
      culture_data = culture.dict(exclude_none=True)
      zones_with_given_id = zones.count({ '_id': zone_id })
      zone_exists = zones_with_given_id == 1

      if zone_exists:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        image_filename = '{}-{}'.format(now, body['image'].filename)
        culture_data['image'] = image_filename

        pymongo_client.save_file(image_filename, body['image'])
        cultures.insert_one(culture_data)

        return GlobalController.generateResponse(HTTP_CREATED_CODE, SUCCESS_MESSAGE, culture_data)

    raise Exception()

  except:
    return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)
