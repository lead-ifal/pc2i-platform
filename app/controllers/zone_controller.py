import requests
from bson import ObjectId
from config import Config
from flask import request
from typing import Collection
from app.extensions import database, mqtt
from app.middlewares.has_token import has_token
from app.middlewares.check_mongodb_id import check_mongodb_id
from app.middlewares.access_control import access_control
from app.controllers.global_controller import GlobalController
from app.models.irrigation_zone import IrrigationZone
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
    ZONE_NOT_FOUND_MESSAGE,
    INTERNAL_SERVER_ERROR_MESSAGE,
)
from app.constants.required_params import required_params

cultures: Collection = database.db.cultures
irrigation_zones: Collection = database.db.irrigation_zones
scheduled_irrigations: Collection = database.db.scheduled_irrigations
mqtt: mqtt


class ZoneController:
    irrigation_status = False

    @has_token
    def create():
        body = request.get_json()
        params = required_params["irrigation_zones"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)
        try:
            if includes_params:
                body["cultures"] = []
                body["schedules"] = []
                body["user_id"] = ObjectId(body["user_id"])
                irrigation_zone = IrrigationZone(**body)
                irrigation_zone_data = irrigation_zone.dict(exclude_none=True)

                irrigation_zones.insert_one(irrigation_zone_data)

                return GlobalController.generate_response(
                    HTTP_CREATED_CODE, SUCCESS_MESSAGE, irrigation_zone_data
                )

                raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    @access_control
    @check_mongodb_id
    @has_token
    def delete(irrigation_zone_id):
        try:
            irrigation_zones.find_one_and_delete({"_id": ObjectId(irrigation_zone_id)})
            cultures.delete_many({"irrigation_zone_id": irrigation_zone_id})
            scheduled_irrigations.delete_many(
                {"irrigation_zone_id": irrigation_zone_id}
            )
            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_zone_id
            )

            raise Exception()
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @access_control
    @check_mongodb_id
    @has_token
    def update(irrigation_zone_id):
        """
        Update an irrigation zone
        ---
        tags:
          - Irrigation Zones
        parameters:
          - name: token
            in: header
            description: Authentication key
          - name: data
            description: Updated irrigation zone
            in: body
            schema:
              id: Irrigation Zone
              properties:
                irrigation_zone_id:
                  required: true
                  description: MongoDB ObjectID for irrigation zone
                  type: string
                user_id:
                  required: true
                  description: MongoDB ObjectID for user
                  type: string
                name:
                  required: true
                  description: Irrigation zone name
                  type: string
                description:
                  required: true
                  description: Irrigation zone description
                  type: string
                size:
                  required: true
                  description: Irrigation zone size
                  type: number
                  format: float
                irrigation_type:
                  required: true
                  description: Irrigation type
                  type: number
        responses:
          200:
            description: Success
          400:
            description: Invalid data
          401:
            description: Unauthorized
          500:
            description: Internal server error
        """
        body = request.get_json()
        params = required_params["irrigation_zones"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)
        try:
            if includes_params:
                body["user_id"] = ObjectId(body["user_id"])
                irrigation_zone = IrrigationZone(**body)
                irrigation_zone_data = irrigation_zone.dict(exclude_none=True)
                irrigation_zones.find_one_and_update(
                    {"_id": ObjectId(irrigation_zone_id)},
                    {"$set": irrigation_zone_data},
                )
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_zone_id
                )

            raise Exception()
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    def show(zone_id):
        try:
            irrigation_zone = None

            irrigation_zone = irrigation_zones.find_one({"_id": ObjectId(zone_id)})
            if irrigation_zone != None:
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_zone
                )
            return GlobalController.generate_response(
                HTTP_NOT_FOUND_CODE, ZONE_NOT_FOUND_MESSAGE
            )
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    def list(user_id):
        irrigation_zone_list = irrigation_zones.find({"user_id": ObjectId(user_id)})
        data = []

        for irrigation_zone in irrigation_zone_list:
            data.append(irrigation_zone)

        return GlobalController.generate_response(
            HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
        )

    def toggle_irrigation(zone_id=None):
        ZoneController.irrigation_status = not ZoneController.irrigation_status
        requests.get(
            Config.PC2I_ESP_ADDRESS
            + "/irrigation/"
            + str(ZoneController.irrigation_status)
        )
