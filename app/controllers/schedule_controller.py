from bson import ObjectId
from bson import ObjectId
from flask import request
from typing import Collection
from app.extensions import database
from app.middlewares.check_mongodb_id import check_mongodb_id
from app.middlewares.has_token import has_token
from app.models.schedule_irrigation import ScheduleIrrigation
from app.controllers.global_controller import GlobalController
from app.constants.status_code import (
    HTTP_BAD_REQUEST_CODE,
    HTTP_CREATED_CODE,
    HTTP_SUCCESS_CODE,
    HTTP_SERVER_ERROR_CODE,
)
from app.constants.response_messages import (
    ERROR_MESSAGE,
    SUCCESS_MESSAGE,
    INTERNAL_SERVER_ERROR_MESSAGE,
)
from app.constants.required_params import required_params

scheduled_irrigations: Collection = database.db.scheduled_irrigations


class ScheduleController:
    @check_mongodb_id
    @has_token
    def update_schedule(schedule_id):
        body = request.get_json()
        params = required_params["irrigation_zones"]["schedule"]
        includes_params = GlobalController.includes_all_required_params(params, body)
        try:
            if includes_params:
                body["irrigation_zone_id"] = ObjectId(body["irrigation_zone_id"])
                scheduling = ScheduleIrrigation(**body)
                schedule_irrigation_data = scheduling.dict(exclude_none=True)
                scheduled_irrigations.find_one_and_update(
                    {"_id": ObjectId(schedule_id)},
                    {"$set": schedule_irrigation_data},
                )
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, schedule_id
                )

            raise Exception()
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    @has_token
    def delete_schedule(schedule_id):
        try:
            scheduled_irrigations.find_one_and_delete({"_id": ObjectId(schedule_id)})
            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, schedule_id
            )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @has_token
    def schedule_irrigation():
        body = request.get_json()
        params = required_params["irrigation_zones"]["schedule"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:
            if includes_params:
                body["irrigation_zone_id"] = ObjectId(body["irrigation_zone_id"])
                scheduling = ScheduleIrrigation(**body)
                schedule_irrigation_data = scheduling.dict(exclude_none=True)
                scheduled_irrigations.insert_one(schedule_irrigation_data)

                return GlobalController.generate_response(
                    HTTP_CREATED_CODE, SUCCESS_MESSAGE, schedule_irrigation_data
                )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    @check_mongodb_id
    def schedule_irrigation_list(zone_id):
        try:
            filter = {"irrigation_zone_id": ObjectId(zone_id)}
            schedule_irrigation_zone_list = scheduled_irrigations.find(filter)
            data = []

            for schedule in schedule_irrigation_zone_list:
                data.append(schedule)

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
            )
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )
