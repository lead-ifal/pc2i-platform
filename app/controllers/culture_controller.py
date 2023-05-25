from flask import request
from bson import ObjectId
from datetime import datetime
from app.extensions import database
from app.controllers.global_controller import GlobalController
from app.middlewares.check_mongodb_id import check_mongodb_id
from app.middlewares.has_token import has_token
from app.models.culture import Culture
from app.constants.status_code import (
    HTTP_BAD_REQUEST_CODE,
    HTTP_CREATED_CODE,
    HTTP_SUCCESS_CODE,
    HTTP_NOT_FOUND_CODE,
    HTTP_SERVER_ERROR_CODE,
)
from app.constants.response_messages import (
    ERROR_MESSAGE,
    SUCCESS_MESSAGE,
    CULTURE_NOT_FOUND_MESSAGE,
    INTERNAL_SERVER_ERROR_MESSAGE,
)
from app.constants.required_params import required_params
from typing import Collection

cultures: Collection = database.db.cultures
irrigation_zones: Collection = database.db.irrigation_zones


class CultureController:
    @has_token
    def create():
        body = {**request.form.to_dict(), **request.files.to_dict()}
        params = required_params["cultures"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:
            if includes_params:
                body["irrigation_zone_id"] = ObjectId(body["irrigation_zone_id"])
                body["planting_date"] = datetime.fromisoformat(body["planting_date"])
                body["geographic_coordinates"] = {
                    "type": "Point",
                    "coordinates": body["geographic_coordinates"],
                }

                if "harvest_date" in body:
                    body["harvest_date"] = datetime.fromisoformat(body["harvest_date"])

                culture = Culture(**body)
                culture_data = culture.dict(exclude_none=True)
                filter = {"_id": body["irrigation_zone_id"]}
                irrigation_zone_exists = irrigation_zones.count(filter) == 1

                if irrigation_zone_exists:
                    if "image" in body:
                        now = datetime.now().strftime("%Y%m%d%H%M%S")
                        image_filename = "{}-{}".format(now, body["image"].filename)
                        culture_data["image"] = image_filename

                        database.save_file(image_filename, body["image"])

                    cultures.insert_one(culture_data)

                    return GlobalController.generate_response(
                        HTTP_CREATED_CODE, SUCCESS_MESSAGE, culture_data
                    )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    @check_mongodb_id
    @has_token
    def delete(culture_id):
        try:
            cultures.find_one_and_delete({"_id": ObjectId(culture_id)})
            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, culture_id
            )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    @has_token
    def update(culture_id):
        body = {**request.form.to_dict(), **request.files.to_dict()}
        params = required_params["cultures"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:
            if includes_params:
                body["planting_date"] = datetime.fromisoformat(body["planting_date"])
                body["geographic_coordinates"] = {
                    "type": "Point",
                    "coordinates": body["geographic_coordinates"],
                }

                if "harvest_date" in body:
                    body["harvest_date"] = datetime.fromisoformat(body["harvest_date"])

                body["irrigation_zone_id"] = ObjectId(body["irrigation_zone_id"])
                culture = Culture(**body)
                culture_data = culture.dict(exclude_none=True)
                if "image" in body:
                    now = datetime.now().strftime("%Y%m%d%H%M%S")
                    image_filename = "{}-{}".format(now, body["image"].filename)
                    culture_data["image"] = image_filename
                    database.save_file(image_filename, body["image"])
                cultures.find_one_and_update(
                    {"_id": ObjectId(culture_id)}, {"$set": culture_data}
                )
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, culture_data
                )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    def list(irrigation_zone_id):
        try:
            culture_list = cultures.find(
                {"irrigation_zone_id": ObjectId(irrigation_zone_id)}
            )
            data = []

            for culture in culture_list:
                data.append(culture)

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
            )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    def show(culture_id):
        try:
            data = None

            data = cultures.find_one({"_id": ObjectId(culture_id)})

            if data != None:
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
                )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )
