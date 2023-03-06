from typing import Collection
from flask import request
from app.controllers.global_controller import GlobalController
from app.middlewares.has_token import has_token
from app.extensions import database
from app.constants.required_params import required_params
from app.models.sensor_type import SensorType
from app.constants.status_code import (
    HTTP_BAD_REQUEST_CODE,
    HTTP_CREATED_CODE,
    HTTP_SUCCESS_CODE,
    HTTP_SERVER_ERROR_CODE,
)
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE

sensor_types: Collection = database.db.sensor_types


class SensorTypeConstroller:
    @has_token
    def create():
        body = request.get_json()
        params = required_params["sensor_types"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:

            if includes_params:
                sensor_type = SensorType(**body)
                result = sensor_types.insert_one(sensor_type.dict(exclude_none=True))
                sensor_type_data = sensor_type.dict(exclude_none=True)
                sensor_type_data["_id"] = result.inserted_id

                return GlobalController.generate_response(
                    HTTP_CREATED_CODE, SUCCESS_MESSAGE, sensor_type_data
                )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    def list():

        try:

            sensor_types_list = sensor_types.find({})
            data = []
            for sensor_type in sensor_types_list:
                data.append(sensor_type)

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
            )

        except:

            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, ERROR_MESSAGE
            )
