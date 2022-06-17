from flask import request
from bson import ObjectId
from datetime import datetime
from app.controllers.global_controller import GlobalController
from app.models.culture import Culture
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from app.constants.required_params import required_params
from typing import Collection
from app import database, pymongo_client

cultures: Collection = database.cultures
irrigation_zones: Collection = database.irrigation_zones

class CultureController:
  def create():
    body = { **request.form.to_dict(), **request.files.to_dict() }
    params = required_params['cultures']['create']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:
        body['planting_date'] = datetime.fromisoformat(body['planting_date'])
        body['geographic_coordinates'] = {
          'type': 'Point',
          'coordinates': body['geographic_coordinates']
        }

        if 'harvest_date' in body:
          body['harvest_date'] = datetime.fromisoformat(body['harvest_date'])

        culture = Culture(**body)
        irrigation_zone_id = ObjectId(culture.irrigation_zone_id)
        culture_data = culture.dict(exclude_none=True)
        irrigation_zone_exists = irrigation_zones.count({ '_id': irrigation_zone_id }) == 1

        if irrigation_zone_exists:
          if 'image' in body:
            now = datetime.now().strftime('%Y%m%d%H%M%S')
            image_filename = '{}-{}'.format(now, body['image'].filename)
            culture_data['image'] = image_filename

            pymongo_client.save_file(image_filename, body['image'])

          cultures.insert_one(culture_data)

          return GlobalController.generate_response(HTTP_CREATED_CODE, SUCCESS_MESSAGE, culture_data)

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

  def list(irrigation_zone_id):
    culture_list = cultures.find({ 'irrigation_zone_id': irrigation_zone_id })
    data = []

    for culture in culture_list:
      data.append(culture)

    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)
