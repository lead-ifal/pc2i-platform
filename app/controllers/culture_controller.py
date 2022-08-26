from flask import request
from bson import ObjectId
from datetime import datetime
from app.extensions import database
from app.controllers.global_controller import GlobalController
from app.middlewares.has_token import has_token
from app.models.culture import Culture
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE, HTTP_NOT_FOUND_CODE, \
  HTTP_SERVER_ERROR_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE, CULTURE_NOT_FOUND_MESSAGE, \
  INTERNAL_SERVER_ERROR_MESSAGE
from app.constants.required_params import required_params
from typing import Collection


cultures: Collection = database.db.cultures
irrigation_zones: Collection = database.db.irrigation_zones

class CultureController:
  @has_token
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

            database.save_file(image_filename, body['image'])

          cultures.insert_one(culture_data)

          return GlobalController.generate_response(HTTP_CREATED_CODE, SUCCESS_MESSAGE, culture_data)

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

  @has_token
  def delete():
    body = request.get_json()
    params = required_params['cultures']['delete']
    includes_params = GlobalController.includes_all_required_params(params, body)
    try:
      if includes_params:
        culture_exists = False
        id = body["culture_id"]
        valid_id = GlobalController.is_valid_mongodb_id(id)
        if valid_id:
          culture_exists = cultures.count({'_id': ObjectId(id)}) == 1
        if culture_exists:
          cultures.delete_one({'_id': ObjectId(id)})

          return GlobalController.generate_response(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            id
          )
        else:
          return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, CULTURE_NOT_FOUND_MESSAGE)

      raise Exception()
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE)

  @has_token
  def edit():
    body = {**request.form.to_dict(), **request.files.to_dict()}
    params = required_params['cultures']['update']
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

        culture_exists = False
        id = body["culture_id"]
        valid_id = GlobalController.is_valid_mongodb_id(id)
        if valid_id:
          culture_exists = cultures.count({'_id': ObjectId(id)}) == 1

        if culture_exists:
          body.pop("culture_id")
          culture = Culture(**body)
          culture_data = culture.dict(exclude_none=True)
          if 'image' in body:
            now = datetime.now().strftime('%Y%m%d%H%M%S')
            image_filename = '{}-{}'.format(now, body['image'].filename)
            culture_data['image'] = image_filename

            database.save_file(image_filename, body['image'])

          cultures.update_one({'_id': ObjectId(id)}, {"$set": culture_data})
          return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, culture_data)
        else:
          return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, CULTURE_NOT_FOUND_MESSAGE)

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

  def list(irrigation_zone_id):
    culture_list = cultures.find({ 'irrigation_zone_id': irrigation_zone_id })
    data = []

    for culture in culture_list:
      data.append(culture)

    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)



  def show(culture_id):
    try:
      data = None
      valid_id = GlobalController.is_valid_mongodb_id(culture_id)
      if valid_id:
        data = cultures.find_one({'_id': ObjectId(culture_id)})
        if data != None:
          return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)
      return GlobalController.generate_response(HTTP_NOT_FOUND_CODE, CULTURE_NOT_FOUND_MESSAGE)
    except:
      return GlobalController.generate_response(HTTP_SERVER_ERROR_CODE,INTERNAL_SERVER_ERROR_MESSAGE)
